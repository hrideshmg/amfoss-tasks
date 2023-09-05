from dotenv import load_dotenv
from inspect import cleandoc
import os
import discord
from discord import app_commands
from scraper import Scraper
import csv

# Loads all environment variables defined in .env
load_dotenv()
token = os.environ.get("token")

# Initializes the scraper
myScraper = Scraper()

# An intent allows the bot to subscribe to a specific bucket of events
intents = discord.Intents.default()
intents.message_content = True
game = discord.Game("Use /help")
client = discord.Client(intents=intents, activity=game)

# Command tree is a container which holds slash command information
client_tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await client_tree.sync()
    print(f"We have logged in as {client.user}")


@client_tree.command(description="Get details about the current live match")
async def livescore(interaction: discord.Interaction):
    match_details = myScraper.get_match()
    message_body = f"Current Match Is Between **{match_details['team1']}** and **{match_details['team2']}**\n"

    if match_details["live"]:
        if match_details["overs_parsed"] and match_details["runs_parsed"]:
            # Clean doc removes indentation from multi line strings
            message_body += cleandoc(
                f"""
                {match_details[match_details["batting"]]} is currently batting with {match_details[match_details["batting"]+"_runs"]} runs taken with {match_details[match_details["batting"]+"_wickets"]} wickets down
                Current over is {match_details["over_current"]} and {match_details["over_finished"]}/{match_details["over_total"]} overs have been finished
                """
            )
            # I.e. if team1 has finished batting
            if match_details["batting"] == "team2":
                message_body += f"\n\n{match_details['team2']} needs {match_details['team1_runs'] - match_details['team2_runs']} more runs from {match_details['over_total'] - match_details['over_finished']} overs"

        elif match_details["overs_parsed"]:
            message_body += cleandoc(
                f"""
                Current over is {match_details["over_current"]} and {match_details["over_finished"]}/{match_details["over_total"]} overs have been finished
                Something went wrong while fetching the runs, please try again later
                """
            )

        elif match_details["runs_parsed"]:
            message_body += cleandoc(
                f"""
                {match_details[match_details["batting"]]} is currently batting with {match_details[match_details["batting"]+"_runs"]} runs taken with {match_details[match_details["batting"]+"_wickets"]} wickets down
                Something went wrong while fetching the overs, please try again later
                """
            )

        else:
            message_body = f"Current Match Is Between **{match_details['team1']}** and **{match_details['team2']}**\nSomething went wrong while fetching the runs and overs, please try again later"
    else:
        message_body = f"There is currently no live match!\nThe next {myScraper.get_upcoming_match()}"

    # Saves a snapshot of the match details to a csv file
    with open("history.csv", "a+") as file:
        writer = csv.writer(file)
        writer.writerow(match_details.values())

    await interaction.response.send_message(message_body)


@client_tree.command(description="Predict the outcome of the current live match")
async def predict(interaction: discord.Interaction):
    match_details = myScraper.get_match()
    if match_details["batting"] == "team2" and match_details["over_finished"] > 0:
        current_run_rate = match_details["team2_runs"] / match_details["over_finished"]
        target_run_rate = (
            match_details["team1_runs"] + 1 - match_details["team2_runs"]
        ) / (match_details["over_total"] - match_details["over_finished"])

        if current_run_rate >= target_run_rate:
            await interaction.response.send_message(
                f"{match_details['team2']} is likely to win"
            )

        if match_details["team2_wickets"] >= 7:
            await interaction.response.send_message(
                f"{match_details['team1']} is likely to win"
            )

        else:
            await interaction.response.send_message(
                f"It's a close match, the outcome is unpredictable"
            )
    else:
        await interaction.response.send_message(
            f"Prediction engine is unavailable until the first inning is over"
        )


@client_tree.command(description="Retrieve the command history as a csv file")
async def history(interaction: discord.Interaction):
    file = discord.File("history.csv")
    await interaction.response.send_message(file=file)


@client_tree.command(description="Get information about CricketMaid")
async def help(interaction: discord.Interaction):
    description = cleandoc(
        """
    CricketMaid is a discord bot written in python using discord.py that makes use of beautifulsoup4 to scrape realtime cricket data from https://www.espncricinfo.com/
    It makes use of the slash commands feature of discord in order to provide an easy to use interface.
    
    **Commands**
    `/livescore` - Fetches the live details of the match
    `/predict` - Predicts the result of the current match based on run rate and wickets taken
    `/history` - Returns a csv file listing the livescore command history
    `/help` - Diplays this guide
    """
    )

    embed = discord.Embed(
        title="General Help", colour=discord.Colour.blue(), description=description
    )
    embed.set_author(name=client.user.name)
    embed.set_thumbnail(url=client.user.display_avatar.url)
    await interaction.response.send_message(embed=embed)


client.run(token)

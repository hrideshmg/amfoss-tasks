from bs4 import BeautifulSoup
import requests


class Scraper:
    def _fetch_website(self):
        webpage = requests.get("https://www.espncricinfo.com/live-cricket-score")
        self.soup = BeautifulSoup(webpage.content, "html.parser")

    def _fetch_common_details(self):
        self.match_div = self.soup.find("div", class_="ds-text-compact-xxs")

        header = self.match_div.find(
            "span", class_="ds-text-tight-xs ds-font-bold ds-uppercase ds-leading-5"
        ).string

        status = self.match_div.find(
            "p",
            class_="ds-text-tight-s ds-font-regular ds-truncate ds-text-typo",
        ).string

        team1, team2 = [
            tag.string
            for tag in self.match_div.find(
                "div", class_="ds-flex ds-flex-col ds-mt-2 ds-mb-2"
            ).find_all("p")
        ]

        common_match_details = {
            "team1": team1,
            "team2": team2,
            "header": header,
            "status": status,
        }
        return common_match_details

    def _fetch_live_details(self):
        try:
            live_match_details = {}
            overs = self.match_div.find_all(
                "span", class_="ds-text-compact-xs ds-mr-0.5"
            )
            # There are two spans which contain overs, only one of them will be populated at a time depending on which team is batting.
            for over in overs:
                if over.string != None:
                    over_str = over.string

            # Parse the string to separate the data inside.
            if "." in over_str:
                over_current = int(
                    over_str[over_str.index(".") + 1 : over_str.index("/")]
                )
                over_finished = int(
                    over_str[over_str.index("(") + 1 : over_str.index(".")]
                )
            else:
                over_current = 0
                over_finished = int(
                    over_str[over_str.index("(") + 1 : over_str.index("/")]
                )
            over_total = int(
                over_str[over_str.index("/") + 1 : over_str.index("ov") - 1]
            )

            live_match_details.update(
                {
                    "overs_parsed": True,
                    "over_current": over_current,
                    "over_finished": over_finished,
                    "over_total": over_total,
                }
            )
        except:
            live_match_details.update({"overs_parsed": False})

        try:
            runs_wickets_list = self.match_div.find_all("strong")
            # List will have 2 items if team1 has finished batting
            if len(runs_wickets_list) == 2:
                team1_str = runs_wickets_list[0].string
                team1_runs = (
                    int(team1_str[: team1_str.index("/")])
                    if "/" in team1_str
                    else int(team1_str)
                )
                team2_str = runs_wickets_list[1].string
                team2_runs = (
                    int(team2_str[: team2_str.index("/")])
                    if "/" in team2_str
                    else int(team2_str)
                )
                team2_wickets = int(team2_str[team2_str.index("/") + 1 :])

                live_match_details.update(
                    {
                        "batting": "team2",
                        "runs_parsed": True,
                        "team1_runs": team1_runs,
                        "team2_runs": team2_runs,
                        "team2_wickets": team2_wickets,
                    }
                )
            else:
                team1_str = runs_wickets_list[0].string
                team1_runs = (
                    int(team1_str[: team1_str.index("/")])
                    if "/" in team1_str
                    else int(team1_str)
                )
                team1_wickets = (
                    int(team1_str[team1_str.index("/") + 1 :])
                    if "/" in team1_str
                    else int(team1_str)
                )

                live_match_details.update(
                    {
                        "batting": "team1",
                        "runs_parsed": True,
                        "team1_runs": team1_runs,
                        "team1_wickets": team1_wickets,
                    }
                )
        except:
            live_match_details.update({"runs_parsed": False})

        return live_match_details

    def get_upcoming_match(self):
        try:
            self._fetch_website()
            self._fetch_common_details()
            status = self.match_div.find(
                "p",
                class_="ds-text-tight-s ds-font-regular ds-truncate ds-text-typo",
            )
            time_data = status.find("span")
            # Cleans up the upcoming match string
            return " ".join([x.strip() for x in time_data.get_text().split()]).lower()
        except:
            return "Something went wrong while fetching the upcoming match, please try again later"

    def get_match(self):
        self._fetch_website()
        match_details = self._fetch_common_details()

        # Checks if match is live
        if any(
            kw in match_details["header"].lower()
            for kw in ["live", "delayed", "break", "stumps", "tea"]
        ):
            match_details.update(self._fetch_live_details())
            match_details.update({"live": True})
        else:
            match_details.update({"live": False})

        return match_details


if __name__ == "__main__":
    myScraper = Scraper()
    print(myScraper.get_match())

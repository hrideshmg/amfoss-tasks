for _ in range(int(input())):
    grid = []
    for i in range(3):
        grid.extend(input())
    
    winner = "DRAW"
    winning_combos = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    
    for combo in winning_combos:
        num1,num2,num3 = combo
        if grid[num1] == grid[num2] == grid[num3] and grid[num1] != ".":
            winner = grid[num1]
    print(winner)
                    

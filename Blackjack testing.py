import random

Cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

random.shuffle(Cards)
p1 = [Cards.pop(), Cards.pop()]
p2 = [Cards.pop(), Cards.pop()]

print("Player 1:", p1)
print("Player 2:", "*" ,p2[1])

p1_stay = False
p2_stay = False


while True:
    
    
    if p1_stay == True and p2_stay == True:
        break

   
    if p1_stay == False:
        action = input("\nPlayer 1, do you want to hit or stay? (h/s): ")
        
        if action.lower() == 'h':
            p1.append(Cards.pop())
            print("Player 1 draws a card:", p1[-1])
            print("Player 1 total is now:", sum(p1))
            
           
            if sum(p1) >= 21:
                break
        else:
            print("Player 1 decides to stay.")
            p1_stay = True
            
    if sum(p2)<17:
         p2.append(Cards.pop())
         print("Player 2 draws a card:", p2[-1])
         print("Player 2 total is now:", sum(p2))
    elif sum(p2)>21:
        print("Player 2 busts! Player 1 wins!")
        break
    else:
        print("Player 2 decides to stay.")
        p2_stay = True

 
p1_total = sum(p1)
p2_total = sum(p2)

if p1_total > 21:
    print("Player 1 busts! Player 2 wins!")
elif p2_total > 21:
    print("Player 2 busts! Player 1 wins!")
elif p1_total == 21:
    print("Player 1 has Blackjack! Player 1 wins!")
elif p2_total == 21:
    print("Player 2 has Blackjack! Player 2 wins!")
elif p1_total > p2_total:
    print("Player 1 has a higher score. Player 1 wins!")
elif p2_total > p1_total:
    print("Player 2 has a higher score. Player 2 wins!")
else:
    print("It's a tie!")
    """FIXED THE BUGS:"""
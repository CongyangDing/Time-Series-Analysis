import random


def setup_bricks():
    # create a main pile with 60 bricks
    main_pile = list(range(1, 61))
    # create a discard pile of 0 bricks
    discard_pile = []
    return main_pile, discard_pile


def shuffle_bricks(bricks):
    # shuffle the given bricks
    random.shuffle(bricks)
    return


def check_bricks(main_pile, discard_pile):
    """
    check if there are any bricks left in the given main pile,
    if not, shuffle the discard pile and move the bricks to the main pile
    then, turn over the top brick to be the start of the new discard pile
    """
    if len(main_pile) == 0:
        random.shuffle(discard_pile)
        main_pile.extend(discard_pile)
        discard_pile.clear()
        discard_pile.append(main_pile.pop(0))
    return


def check_tower_blaster(tower):
    # check stability
    for i in range(9):
        if tower[i] > tower[i + 1]:
            return False
    return True


def get_top_brick(brick_pile):
    # take the top brick
    return brick_pile.pop(0)


def deal_initial_bricks(main_pile):
    player_pile = []
    computer_pile = []
    for i in range(10):
        computer_pile.append(main_pile.pop(0))
        player_pile.append(main_pile.pop(0))
    computer_pile.reverse()
    player_pile.reverse()
    return computer_pile, player_pile


def add_brick_to_discard(brick, discard_pile):
    discard_pile.insert(0, brick)
    return


def find_and_replace(new_brick, brick_to_be_replaced, tower, discard_pile):
    for i in range(10):
        if tower[i] == brick_to_be_replaced:
            # tower.pop(i)
            # tower.insert(i,new_brick)
            tower[i] = new_brick
            discard_pile.insert(0, brick_to_be_replaced)
            return True
    return False


def computer_play(tower, main_pile, discard_pile):
    max_score = 0
    replace_brick = -1
    current_score = order_score(tower)
    rand_res = random.randint(1, 10)
    if rand_res == 1 or rand_res == 2:  # sometimes you just want to trust your luck
        print("Computer wants to try it's luck")
        main_pile_brick = main_pile[0]
        print(f"Computer tried main_pile and the top of main_pile is {main_pile_brick}")
        for i in range(10):
            tmp = tower[i]
            tower[i] = main_pile_brick
            tmp_score = order_score(tower)
            if tmp_score > max_score:
                max_score = tmp_score
                replace_brick = tmp
            tower[i] = tmp
        if max_score > current_score + 0.15:
            find_and_replace(get_top_brick(main_pile), replace_brick, tower, discard_pile)
            print(f"The computer replaced {replace_brick} with {main_pile_brick}")
            # print("Computer's Tower: ",tower)
        else:
            add_brick_to_discard(main_pile.pop(0), discard_pile)
            print(f"Computer tried main_pile and the top of main_pile is {main_pile_brick}")
            print("The computer didn't change it's brick")
    else:  # now you are just realistic. consider the discard_pile first.
        discard_brick = discard_pile[0]
        for i in range(10):
            tmp = tower[i]
            tower[i] = discard_brick
            tmp_score = order_score(tower)
            if tmp_score > max_score:
                max_score = tmp_score
                replace_brick = tmp
            tower[i] = tmp
        if max_score > current_score + 0.35:
            find_and_replace(get_top_brick(discard_pile), replace_brick, tower, discard_pile)
            print(f"The computer replaced {replace_brick} with {discard_brick}")
            # print("Computer's Tower: ",tower)
        else:  # if the brick in discard_pile is not satisfying, you will try your luck in the main_pile
            main_pile_brick = main_pile[0]
            print(f"Computer tried main_pile and the top of main_pile is {main_pile_brick}")
            for i in range(10):
                tmp = tower[i]
                tower[i] = main_pile_brick
                tmp_score = order_score(tower)
                if tmp_score > max_score:
                    max_score = tmp_score
                    replace_brick = tmp
                tower[i] = tmp
            if max_score > current_score + 0.35:
                find_and_replace(get_top_brick(main_pile), replace_brick, tower, discard_pile)
                print(f"The computer replaced {replace_brick} with {main_pile_brick}")
                # print("Computer's Tower: ",tower)
            else:
                add_brick_to_discard(main_pile.pop(0), discard_pile)
                print("The computer didn't change it's brick")
    return


def order_score(tower):
    # use the maximum number as one part of judgement score
    # punish small number which close to the bottom, vice versa
    lamda = 0.07  # loss coefficient
    max_ordered = 1
    res = 1
    end = 1
    order_loss = 0
    # max_order_loss = 0
    for i in range(1, len(tower)):
        if tower[i] > tower[i - 1]:
            max_ordered += 1
            if max_ordered > res:
                end = i
                res = max_ordered
        else:
            max_ordered = 1
    head = end - res + 1
    for i in range(head, end + 1):
        order_loss += abs(tower[i] - i * 6)
    order_loss /= res
    order_loss *= lamda
    # print(order_loss)
    return res - order_loss


def main():
    main_pile, discard_pile = setup_bricks()
    shuffle_bricks(main_pile)
    computer_pile, player_pile = deal_initial_bricks(main_pile)
    print("The computer tower is : ", computer_pile)
    print("Your tower is : ", player_pile)
    print('*' * 60)
    add_brick_to_discard(main_pile.pop(0), discard_pile)
    while 1:
        check_bricks(main_pile, discard_pile)
        print("COMPUTER'S TURN")
        print(f"The top brick on discard pile is {discard_pile[0]}")
        computer_play(computer_pile, main_pile, discard_pile)
        check_bricks(main_pile, discard_pile)
        if check_tower_blaster(computer_pile):
            print("Computer won the game!")
            break
        # print("COMPUTER DID NOTHING")
        print('*' * 60)
        print("NOW IT'S YOUR TURN!")
        print("Your Tower: ", player_pile)
        print(f"The top brick on discard pile is {discard_pile[0]}")
        print('*' * 60)
        print("Type 'D' to take discard brick,'M' for a mystery brick, or 'H' for help")
        while 1:
            user_type = input()
            if user_type == 'm' or user_type == 'M':
                item = get_top_brick(main_pile)
                print(f"You picked {item} from main pile")
                print("Do you want to use this brick? Type 'Y' or 'N' to skip turn")
                user_confirm = input()
                if user_confirm == 'y' or user_confirm == 'Y':
                    print("Where do you want to replace this brick? Type a brick number to replace in your tower.")
                    while not find_and_replace(item, int(input()), player_pile, discard_pile):
                        print("Brick not found, type the brick again")
                    # brick_to_be_replace = int(input()) #need to check if exist
                    # find_and_replace(item,brick_to_be_replace,player_pile,discard_pile)
                    print(f"You replaced {discard_pile[0]} with {item}")
                else:
                    add_brick_to_discard(item, discard_pile)
                print("Your Tower: ", player_pile)
                break
            if user_type == 'd' or user_type == 'D':
                item = get_top_brick(discard_pile)
                print(f"You picked {item} from discard pile")
                print("Where do you want to replace this brick? Type a brick number to replace in your tower.")
                while not find_and_replace(item, int(input()), player_pile, discard_pile):
                    print("Brick not found, type the brick again")
                # brick_to_be_replace = int(input()) #need to check if exist
                # find_and_replace(item,brick_to_be_replace,player_pile,discard_pile)
                print(f"You replaced {discard_pile[0]} with {item}")
                print("Your Tower: ", player_pile)
                break
            if user_type == 'h' or user_type == 'H':
                print("You can look for help in HW3_CIT5918.pdf")
                print("Please retype")
                continue
            print("Unknown input,please type again")
        print('*' * 60)
        if check_tower_blaster(player_pile):
            print("You won the game!")
            break
        check_bricks(main_pile, discard_pile)
    return


if __name__ == "__main__":
    main()

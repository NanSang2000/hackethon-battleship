def getShipPos():
    '''
    THIS IS THE LIST OF SHIPS
    [5,3,3,2,2] 
    That is: 
    1x 5 long
    2x 3 long
    2x 2 long

    Your ships must satisfy this 
    '''

    # due to a bug we have the indexing of ships are 0-9
    
    shipPos = [[(3,1), (4,1),(5,1)], 
                [(2,1),(2,2),(2,3),(2,4),(2,5)], 
                [(7,7),(8,7)] , 
                [(0,9), (1,9), (2,9)], 
                [(5,9), (6,9)]]
    return shipPos
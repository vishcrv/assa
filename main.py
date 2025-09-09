import sys
from agent.agent import BrowserAgent

def main():
    # check for command line arguments
    fast = '--fast' in sys.argv or '-f' in sys.argv
    
    # get search term
    search_args = [arg for arg in sys.argv[1:] if not arg.startswith('-')]
    
    if search_args:
        search_term = ' '.join(search_args)
    else:
        search_term = input("Enter search term: ")

    # show mode information
    if fast:
        print("[INFO] Running in FAST DEMO mode")

    agent = BrowserAgent()

    # run session
    if fast:
        agent.run_fast_demo(search_term)
    else:
        agent.run(search_term)

    

    """
    main entry function
    1. ask user for a search term
    2. create an instance of BrowserAgent
    3. run the agent with that search term
    """
    


if __name__ == "__main__":
    #call main()
    main()

import networkx as nx
import pandas as pd

class EuropeanFootballMarket:
    """
    A class to represent a European football market.
    """


    def __init__(self):
        """
        Initializes the EuropeanFootballMarket with player data from a CSV file.
        The CSV file should contain player transfer data including player name, position, transfer fee, year, and clubs involved.
        The data is stored in a directed graph where nodes are clubs and edges represent transfers between clubs.
        """
        self.graph = nx.DiGraph()

        self.transfer_files = ['1-bundesliga.csv', 'championship.csv', 'eredivisie.csv', 'premier-liga.csv', 'ligue-1.csv', 
                               'premier-league.csv', 'serie-a.csv', 'liga-nos.csv', 'primera-division.csv']
        
    def read_all_data(self):
        """
        Reads player data from multiple CSV files and constructs a directed graph.

        Returns
        -------
        None
        """
        for file in self.transfer_files:
            self._read_file(file)

    def _read_file(self, file_path):
        """
        Reads a CSV file and constructs a directed graph.

        Parameters
        ----------
        file_path : str
            Path to the CSV file.

        Returns
        -------
        None
        """

        df = pd.read_csv(file_path)

        for _, transfer in df.iterrows():
            if not pd.isna(transfer["fee_cleaned"]):
                player_name = transfer["player_name"]
                position = transfer["position"]
                fee = transfer["fee_cleaned"]
                year = transfer["year"]
                if transfer["transfer_movement"] ==  "in":
                    to_club = transfer["club_name"]
                    from_club = transfer["club_involved_name"]
                else:
                    from_club = transfer["club_name"]
                    to_club = transfer["club_involved_name"]

            
                self._add_transfer(from_club, to_club, player_name, position, fee, year)



    def _add_transfer(self, from_club, to_club, player_name, position, fee, year):
        """
        Adds a transfer to the directed graph.

        Parameters
        ----------
        from_club : str
            Name of the club the player is transferring from.
        to_club : str
            Name of the club the player is transferring to.
        player_name : str
            Name of the player.
        position : str
            Position of the player.
        fee : float
            Transfer fee.
        year : int
            Year of transfer.

        Returns
        -------
        None
        """
        transfer_data = {
            "player_name": player_name,
            "position": position,
            "fee": fee,
            "year": year
        }
        if self.graph.has_edge(from_club, to_club):
            self.graph[from_club][to_club]['transfers'].append(transfer_data)
        else:
            self.graph.add_edge(from_club, to_club, transfers=[transfer_data])

    def get_transfers_between(self, from_club, to_club):
        """
        Returns a list of transfers between two clubs.

        Parameters
        ----------
        from_club : str
            Name of the club the player is transferring from.
        to_club : str
            Name of the club the player is transferring to.

        Returns
        -------
        list[dict]
            List of transfers containing player name, position, fee, and year.
        """
        if not self.graph.has_edge(from_club, to_club):
            return []

        transfers = self.graph[from_club][to_club]['transfers']
        return transfers

    def print_transfers_between(self, from_club, to_club):
        """
        Formats the transfer data between two clubs and prints it.

        Parameters
        ----------
        from_club : str
            Name of the club the player is transferring from.
        to_club : str
            Name of the club the player is transferring to.

        Returns
        -------
        list[dict]
            List of transfers containing player name, position, fee, and year.
        """
        transfers = self.get_transfers_between(from_club, to_club)
    
        if not transfers:
            print(f"No direct transfers from {from_club} to {to_club}.")
            return
        
        print(f"Transfers from {from_club} to {to_club}:")
        for transfer in transfers:
            print(f"- {transfer['year']}: {transfer['player_name']} ({transfer['position']}) for €{transfer['fee']}")

    def get_shortest_path(self, from_club, to_club):
        """
        Returns the shortest path between two clubs.

        Parameters
        ----------
        from_club : str
            Name of the club the player is transferring from.
        to_club : str
            Name of the club the player is transferring to.

        Returns
        -------
        list[str]
            List of clubs in the shortest path.
        """
        if from_club not in self.graph.nodes or to_club not in self.graph.nodes:
            print("One or both clubs not found in the network.")
            return []
    
        visited = set()
        queue = [[from_club]]

        while queue:
            path = queue.pop(0)
            current = path[-1]

            if current == to_club:
                return path

            if current not in visited:
                visited.add(current)
                for neighbor in self.graph.successors(current):
                    if neighbor not in visited:
                        new_path = path + [neighbor]
                        queue.append(new_path)

        print(f"No path exists between {from_club} and {to_club}.")
        return []
    
    def most_connected_clubs(self, top_n=10):
        """
        Returns the top clubs with the most connections in the graph.

        Parameters
        ----------
        top_n : int
            Number of top clubs to return.
            Default is 10.
            
        Returns
        -------
        list[tuple[str, int]]
            List of tuples containing club names and their degree (number of connections).
        """
        degrees = self.graph.degree()
        sorted_degrees = sorted(degrees, key=lambda x: x[1], reverse=True)
        return sorted_degrees[:top_n]
    
    def link_wikipedia(self, club_name):
        """
        Returns the Wikipedia link for a given club.

        Parameters
        ----------
        club_name : str
            Name of the club.

        Returns
        -------
        str
            Wikipedia link for the club.
        """
        base_url = "https://en.wikipedia.org/wiki/"
        formatted_name = club_name.replace(" ", "_")
        return f"{base_url}{formatted_name}"










if __name__ == "__main__":
    market = EuropeanFootballMarket()
    market.read_all_data()
    
    print(f"\nLoaded {market.graph.number_of_nodes()} clubs and {market.graph.number_of_edges()} transfer connections.\n")

    while True:
        print("\n--- European Football Transfer Market ---")
        print("1. View transfers between two clubs")
        print("2. Find shortest path between two clubs")
        print("3. Show the most connected clubs")
        print("4. Get Wikipedia link for a club")
        print("Or type 'exit' to quit the program.")

        choice = input("Choose an option (1–4): ")

        if choice == "1":
            from_club = input("Enter the FROM club: ")
            to_club = input("Enter the TO club: ")
            market.print_transfers_between(from_club, to_club)

        elif choice == "2":
            from_club = input("Enter the FROM club: ")
            to_club = input("Enter the TO club: ")
            path = market.get_shortest_path(from_club, to_club)
            if path:
                print(" -> ".join(path))

        elif choice == "3":
            num_clubs = input("How many top clubs do you want to see? (default is 10): ")
            if not num_clubs.isdigit():
                num_clubs = 10
            else:
                num_clubs = int(num_clubs)
            top_clubs = market.most_connected_clubs(num_clubs)
            print("Top connected clubs:")
            for rank, (club, degree) in enumerate(top_clubs, 1):
                print(f"{rank}. {club} - {degree} connections")

        elif choice == "4":
            club = input("Enter the club name: ")
            print(f"Wikipedia link: {market.link_wikipedia(club)}")

        elif choice == "exit":
            break

        else:
            print("Invalid choice. Please select a number from 1 to 5.")



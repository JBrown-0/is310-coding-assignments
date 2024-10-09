
from rich.console import Console
from rich.table import Table
import csv
import os

# Create a Console instance
console = Console()

# Function to display sample data using Rich Table
def show_initial_data():
    console.print("\n[bold cyan]Here is some initial data:[/bold cyan]")

    # Create a sample table
    table = Table(title="Movies")
    table.add_column("Released", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Box Office", justify="right")

    # Add rows to the table
    table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
    table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
    table.add_row("Dec 15, 2017", "Star Wars Ep. VIII: The Last Jedi", "$1,332,539,889")
    table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

    console.print(table)

# Function to ask user for movie data
def get_movie_data():
    movie_title = console.input("[bold yellow]Enter the title of the movie: [/bold yellow]")
    release_date = console.input("[bold yellow]Enter the release date (e.g., Dec 20, 2019): [/bold yellow]")
    box_office = console.input("[bold yellow]Enter the box office earnings (e.g., $1,000,000,000): [/bold yellow]")
    
    return {"title": movie_title, "release_date": release_date, "box_office": box_office}

# Function to confirm and write data
def confirm_data_and_write(movies):
    console.print("\n[bold cyan]Please confirm your movie data:[/bold cyan]")
    for i, movie in enumerate(movies):
        console.print(f"\nMovie {i + 1}: {movie['title']} ({movie['release_date']}) - {movie['box_office']}")

    confirm = console.input("\nIs the above data correct? (y/n): ").lower()
    if confirm == 'y':
        file_path = os.path.join(os.getcwd(), "movies.csv")
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["title", "release_date", "box_office"])
            writer.writeheader()
            writer.writerows(movies)
        console.print(f"\n[bold green]Data saved successfully to {file_path}[/bold green]")
    else:
        console.print("\n[bold red]Re-enter your data.[/bold red]")
        return False
    return True

def main():
    show_initial_data()

    movies = []
    while True:
        movie = get_movie_data()
        movies.append(movie)
        add_more = console.input("\nDo you want to add another movie? (y/n): ").lower()
        if add_more == 'n':
            break

    while not confirm_data_and_write(movies):
        movies.clear()
        console.print("\nLet's re-enter all the data again.\n")
        movies.append(get_movie_data())

if __name__ == "__main__":
    main()


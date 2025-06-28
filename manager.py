import sys
import os

# Add the current directory (project root) to sys.path
# This allows Python to find the 'vpodcasts' package.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "web":
        # Execute the web server's main function
        from vpodcasts.webapp import main
        main()
    else:
        # Delegate to the ypd.py CLI for other commands
        from vpodcasts.ypd import cli
        # Pass all arguments (excluding 'python manager.py') to the click CLI
        # prog_name is set for correct usage display in help messages
        cli.main(args=sys.argv[1:], prog_name="python manager.py")

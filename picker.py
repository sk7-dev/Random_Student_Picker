import pandas as pd
import random
import curses
from datetime import datetime
import copy

def load_students(filename):
    """Load student data from CSV file and return DataFrame."""
    try:
        df = pd.read_csv(filename)
        if 'LastPicked' not in df.columns:
            df['LastPicked'] = None
        if 'PickOrder' not in df.columns:
            df['PickOrder'] = None
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find {filename}. Please ensure it exists.")

def save_students(df, filename):
    """Save the updated student data back to CSV."""
    df.to_csv(filename, index=False)

def pick_student(df):
    """Pick a random student that hasn't been picked yet."""
    # Get students who haven't been picked (LastPicked is None)
    unpicked = df[df['LastPicked'].isna()]
    if len(unpicked) == 0:
        return None, df, None
    
    # Pick a random student
    chosen_idx = random.choice(unpicked.index)
    
    # Calculate next pick order number
    current_max_order = df['PickOrder'].max()
    next_order = 1 if pd.isna(current_max_order) else int(current_max_order) + 1
    
    # Update the LastPicked timestamp and PickOrder
    df.at[chosen_idx, 'LastPicked'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df.at[chosen_idx, 'PickOrder'] = next_order
    
    return df.at[chosen_idx, 'Name'], df, next_order

def draw_box(win, y, x, height, width):
    """Draw a box with double-line borders."""
    win.addch(y, x, '╔')
    win.addch(y, x + width - 1, '╗')
    win.addch(y + height - 1, x, '╚')
    win.addch(y + height - 1, x + width - 1, '╝')
    
    for i in range(1, width - 1):
        win.addch(y, x + i, '═')
        win.addch(y + height - 1, x + i, '═')
    
    for i in range(1, height - 1):
        win.addch(y + i, x, '║')
        win.addch(y + i, x + width - 1, '║')

def display_history(stdscr, df, start_y):
    """Display the last 5 picked students with their timestamps and order."""
    picked = df[df['LastPicked'].notna()].sort_values('LastPicked', ascending=False).head(5)
    if not picked.empty:
        stdscr.addstr(start_y, 4, "Recently Picked:", curses.color_pair(3))
        for i, (_, row) in enumerate(picked.iterrows()):
            time_str = pd.to_datetime(row['LastPicked']).strftime('%H:%M:%S')
            order_str = f"#{int(row['PickOrder'])}" if pd.notna(row['PickOrder']) else "#-"
            display_str = f"{order_str.ljust(4)} {row['Name']} ({time_str})"
            stdscr.addstr(start_y + i + 1, 6, display_str, curses.color_pair(2))

def main(stdscr):
    # Setup
    curses.curs_set(0)  # Hide cursor
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    
    filename = "students.csv"
    df = load_students(filename)
    start_time = datetime.now()
    
    # Store previous state for restore functionality
    previous_state = None
    previous_picked = None
    previous_order = None
    
    # Get terminal dimensions
    max_y, max_x = stdscr.getmaxyx()
    
    while True:
        stdscr.clear()
        
        # Draw main box
        draw_box(stdscr, 1, 2, max_y-2, max_x-4)
        
        # Title
        title = "✨ Random Student Picker ✨"
        stdscr.addstr(3, (max_x - len(title)) // 2, title, curses.color_pair(1) | curses.A_BOLD)
        
        # Instructions
        stdscr.addstr(5, 4, "Press ", curses.color_pair(2))
        stdscr.addstr("ENTER", curses.A_BOLD)
        stdscr.addstr(" to pick a student, ", curses.color_pair(2))
        stdscr.addstr("U", curses.A_BOLD)
        stdscr.addstr(" to undo last pick, ", curses.color_pair(2))
        stdscr.addstr("R", curses.A_BOLD)
        stdscr.addstr(" to reset all, ", curses.color_pair(2))
        stdscr.addstr("Q", curses.A_BOLD)
        stdscr.addstr(" to quit", curses.color_pair(2))
        
        # Statistics
        stats_y = 7
        total_students = len(df)
        picked_students = df['LastPicked'].notna().sum()
        stdscr.addstr(stats_y, 4, f"Total students: {total_students}", curses.color_pair(3))
        stdscr.addstr(stats_y + 1, 4, f"Students picked: {picked_students}", curses.color_pair(3))
        stdscr.addstr(stats_y + 2, 4, f"Remaining: {total_students - picked_students}", curses.color_pair(3))
        
        # Display picked history
        display_history(stdscr, df, stats_y + 4)
        
        # Session duration
        duration = datetime.now() - start_time
        duration_str = f"Session duration: {duration.seconds // 60}m {duration.seconds % 60}s"
        stdscr.addstr(max_y-4, 4, duration_str, curses.color_pair(2))
        
        # Picked student display
        if hasattr(main, 'last_picked'):
            pick_announcement = "PICKED STUDENT:"
            stdscr.addstr(stats_y + 10, (max_x - len(pick_announcement)) // 2, 
                         pick_announcement, curses.color_pair(4) | curses.A_BOLD)
            
            # Include order number in display if available
            display_text = (f"#{main.last_order} - {main.last_picked}" 
                          if hasattr(main, 'last_order') 
                          else main.last_picked)
            
            student_box_width = len(display_text) + 4
            student_box_x = (max_x - student_box_width) // 2
            draw_box(stdscr, stats_y + 11, student_box_x, 3, student_box_width)
            stdscr.addstr(stats_y + 12, student_box_x + 2, display_text, 
                         curses.color_pair(1) | curses.A_BOLD)
        
        stdscr.refresh()
        
        # Handle input
        key = stdscr.getch()
        
        if key == ord('q') or key == ord('Q'):
            break
            
        elif key == ord('r') or key == ord('R'):
            # Store current state before reset
            previous_state = df.copy()
            previous_picked = main.last_picked if hasattr(main, 'last_picked') else None
            previous_order = main.last_order if hasattr(main, 'last_order') else None
            
            # Reset all picks
            df['LastPicked'] = None
            df['PickOrder'] = None
            save_students(df, filename)
            main.last_picked = "ALL STUDENTS RESET"
            if hasattr(main, 'last_order'):
                delattr(main, 'last_order')
            
        elif key == ord('u') or key == ord('U'):
            # Restore previous state if available
            if previous_state is not None:
                df = previous_state.copy()
                save_students(df, filename)
                if previous_picked:
                    main.last_picked = previous_picked
                    if previous_order:
                        main.last_order = previous_order
                    else:
                        delattr(main, 'last_order')
                else:
                    delattr(main, 'last_picked')
                    if hasattr(main, 'last_order'):
                        delattr(main, 'last_order')
                
                # Clear previous state after restore
                previous_state = None
                previous_picked = None
                previous_order = None
            
        elif key == 10:  # Enter key
            # Store current state before new pick
            previous_state = df.copy()
            previous_picked = main.last_picked if hasattr(main, 'last_picked') else None
            previous_order = main.last_order if hasattr(main, 'last_order') else None
            
            student, df, order = pick_student(df)
            
            if student is None:
                main.last_picked = "ALL PICKED - PRESS R TO RESET"
                if hasattr(main, 'last_order'):
                    delattr(main, 'last_order')
            else:
                main.last_picked = student
                main.last_order = order
                save_students(df, filename)

if __name__ == "__main__":
    curses.wrapper(main)
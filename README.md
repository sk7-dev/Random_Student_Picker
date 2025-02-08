# Random Student Picker 🎯

A command-line interface (CLI) tool for randomly selecting students from a class list with persistent tracking and undo functionality. Built using Python with curses for the terminal user interface.

## ✨ Features

### Core Functionality
* Random student selection
* Persistent tracking between sessions
* Pick order history
* One-step undo/restore
* Visual terminal interface
* Session duration tracking
* Real-time statistics

### Display Elements
* Decorated title banner
* Student selection display box
* Recent picks history (last 5)
* Current session statistics
* Clear user instructions
* Session duration timer

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/sk7-dev/Random_Student_Picker.git
cd Random_Student_Picker
```

2. Install required packages:
```bash
pip install pandas curses-menu
```

3. Create your students CSV file (see [File Format](#file-format))

4. Run the program:
```bash
python picker.py
```

## 📖 Usage

1. Prepare your student list in CSV format
2. Run the program
3. Use keyboard controls to:
   * Pick random students
   * Undo mistakes
   * Reset when needed
4. All selections are automatically saved

## 📁 File Format

Create a CSV file named `students.csv` with this structure:

```csv
Name
John Doe
Jane Smith
```

### Column Descriptions:
* `Name`: Student name (required)
* `LastPicked`: Timestamp of selection (program managed)
* `PickOrder`: Selection order number (program managed)

## ⌨️ Controls

| Key | Action |
|-----|--------|
| `ENTER` | Pick random student |
| `Z` | Undo last action |
| `R` | Reset all picks |
| `Q` | Quit program |

### Statistics Panel
* Total student count
* Picked students count
* Remaining students
* Last 5 selections with timestamps

### Features Implementation
1. **History Tracking**
   - Maintains last 5 picks
   - Stores timestamps
   - Tracks pick order

2. **Undo Functionality**
   - One-step restore
   - Covers picks and resets
   - Complete state restoration

3. **Session Management**
   - Duration tracking
   - Cross-session persistence
   - Pick order preservation

## 🛠️ Error Handling
* Missing file detection
* Automatic column creation
* Empty data management
* Duplicate pick prevention

## 🔜 Future Enhancements
- [ ] Multiple undo steps
- [ ] Custom CSV file selection
- [ ] Export session statistics
- [ ] Multiple class list support
- [ ] Customizable display colors

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by sk7-dev

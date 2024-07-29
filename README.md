# Bible Verse and Songs

This project is a Python application designed to display Bible verses and songs on a projector screen. 

The Application allows you to show Bible verse in different languges.
Show song slides in different Languages and translation.
Show Images.

The Bible text is Zefania XML Bible Markup Language.
The songs text with translation provided by "Nachalat Yeshua" congregation.
איק

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python installed on your machine. You can download it from the official website: https://www.python.org/downloads/.

Bible text in Zefania XML Bible Markup Language Format. Can be found on https://sourceforge.net/projects/zefania-sharp/.

Microsoft Power Point for ppt presentation, pptx files doesn't require Power Point.

### Installation

Clone the repository:

```bash
git clone https://github.com/benySuho/Bible-And-Songs.git
```

Navigate to the project directory:

```bash
cd Bible-And-Songs
```


## Usage
Before the run, create Bible, Songs, Presentations, Images folder in the Bible-And-Songs folder.

Add to Bible folder .xml files of Zefania XML Bible Markup Language Files.

Add Power Point Presentation to Presentations folder.

Add your images to Images folder.

Add songs, saved by python pickle to Songs folder.

To run the application, execute the following command:

```bash
python main.py
```

The app will display a GUI with options to select a Bible, Songs, Images. You can also customize the font size, color, and background color of the displayed text.

## Create Executable

To create .exe file, execute the following command:

```bash
python pyinstaller.py
```

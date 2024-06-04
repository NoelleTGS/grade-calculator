# Grade Calculator
Simple grade calculator written in Python. 
### Features
- Calculate overall grade for multiple classes
- Configure different grade types and their weight
- Set individual grade weighting
- Save grades to file to view and edit later
## Usage
Run `main.py` with Python.
```sh
python main.py
```
The first time you run the program, it will create the `grades_data.json` file that your grades will be saved to. Every edit you make to your grades will automatically be saved to the file.

Start by selecting option 5 to create a course, and enter the information for the course. You can then select option 6 to add a new type to your course. If there's only one type or everything is weighted equally, you can simply create a type with a weight of 1.

Add grades to your course by selecting 3, then your course, then your course type.

You can view your overall grades by selecting 1, or select 2 to view an advanced view with each individual assignment and type grades.

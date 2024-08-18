# BMI Calculator

## Overview
This project is a graphical BMI (Body Mass Index) Calculator built using Python's `tkinter` library. The application allows users to input their weight and height, choose their preferred units, and calculate their BMI. It also provides a profile management feature, historical BMI records, data visualization, and other advanced functionalities. The application supports themes, multi-language options, and various user interactions.

## Features
- **BMI Calculation**: Input your weight and height in various units and receive your BMI along with a categorization (Underweight, Normal weight, Overweight, Obesity).
- **Profile Management**: Save and load user profiles including name, age, and gender.
- **History Tracking**: Automatically save your BMI calculation history and load it on application start.
- **Data Visualization**: Plot BMI distribution graphs based on your history.
- **Settings**: Adjust settings like theme (light or dark mode) and language.
- **Feedback**: Submit feedback directly through the application.
- **Advanced Options**: Includes a variety of additional features like data export/import, complex operations, random input simulations, and much more.

## Installation
1. **Clone the repository**:
    ```sh
    git clone https://github.com/pragunsrv/bmi-calculator.git
    cd bmi-calculator
    ```

2. **Install dependencies**:
    Make sure you have Python installed. Install the required Python packages using:
    ```sh
    pip install matplotlib
    ```

3. **Run the application**:
    ```sh
    python bmi_calculator.py
    ```

## Usage
1. **Calculate BMI**:
   - Enter your weight and height.
   - Choose your preferred units (kg/m or lbs/ft).
   - Click "Calculate" to see your BMI and its category.

2. **Profile Management**:
   - Enter your name, age, and gender.
   - Click "Save Profile" to store your details.
   - Load a previously saved profile by clicking "Load Profile".

3. **View History**:
   - Previous BMI calculations are stored in the history list. You can clear this history or apply filters to view specific entries.

4. **Settings**:
   - Access the settings dialog to change the theme or language of the application.

5. **Plot BMI Distribution**:
   - Click the "Plot BMI Distribution" button to visualize your BMI records on a graph.

6. **Additional Features**:
   - Explore the application for more features like exporting/importing data, providing feedback, and more.

## File Structure
- `main.py`: The main Python script for the BMI Calculator application.
- `user_preferences.json`: A file storing user preferences like theme and language.
- `bmi_history.json`: A file storing the history of BMI calculations.
- `README.md`: This file, providing an overview of the project.

## Requirements
- Python 3.x
- `tkinter` (usually comes with Python)
- `matplotlib`

## Contributing
Feel free to fork this repository, make improvements, and submit a pull request. Contributions are welcome!

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- **Python**: For providing the language and standard libraries to build this application.
- **Tkinter**: For the graphical interface.
- **Matplotlib**: For the data visualization capabilities.

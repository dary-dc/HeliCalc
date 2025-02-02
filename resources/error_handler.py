from PyQt5.QtWidgets import QMessageBox
from .dict import warnings, DK_DH_diameters

class ErrorHandler:
    def __init__(self, main_window_object):
        self.main_window = main_window_object
        self.input_data = self.main_window.input_data
        self.design_results = self.main_window.design_results
        self.design_calculator = self.main_window.design_calculator

        self.wrong_style = """background-color: rgb(255, 62, 62);border: 1px solid black;}QLineEdit:hover{background-color:rgb(229, 0, 0);"""
        self.correct_style = """background-color: rgb(0, 255, 0);border: 1px solid black;}QLineEdit:hover{background-color:rgb(0, 170, 0);"""
        self.standard_style = """background-color: rgb(255, 255, 0);border: 1px solid black;}QLineEdit:hover{background-color:rgb(255, 204, 0);"""

    # used in page 3
    # Checks that the fluid names were entered, raising a warning if not.
    # For some reason it was complicated for me to create only one error
    # for the both cases: not entering one of the names or not entering both
    def check_fluids_names(self):
        hot_fluid_name = self.main_window.lineEdit_Name_hot_fluid.text()
        cold_fluid_name = self.main_window.lineEdit_Name_cold_fluid.text()

        if not hot_fluid_name and not cold_fluid_name:
            self.main_window.lineEdit_Name_hot_fluid.setStyleSheet(self.wrong_style)
            self.main_window.lineEdit_Name_cold_fluid.setStyleSheet(self.wrong_style)
            self.warn_serveral_objects([self.main_window.lineEdit_Name_hot_fluid, self.main_window.lineEdit_Name_cold_fluid], "SeveralEmptyLinesError", [self.main_window.lineEdit_Name_hot_fluid, self.main_window.lineEdit_Name_cold_fluid])
            return False
    
        if not hot_fluid_name:
            self.main_window.lineEdit_Name_hot_fluid.setStyleSheet(self.wrong_style)
            self.warn_one_object(self.main_window.lineEdit_Name_hot_fluid.objectName(), "EmptyLineError")
            return False
        self.main_window.lineEdit_Name_hot_fluid.setStyleSheet(self.standard_style)

        if not cold_fluid_name:
            self.main_window.lineEdit_Name_cold_fluid.setStyleSheet(self.wrong_style)
            self.warn_one_object(self.main_window.lineEdit_Name_cold_fluid.objectName(), "EmptyLineError")
            return False
        self.main_window.lineEdit_Name_cold_fluid.setStyleSheet(self.standard_style)

        return True
    
    # Check one of the radio buttons in the buttonGroup was selected,
    # raising an error if not. It is used in the method check_page_3_data
    def test_radio_button_selected(self):
        selected = self.main_window.buttonGroup.checkedButton()
        if not selected:
            self.warn_one_object("", "SelectionError")
            return False
        return True        

    # used in page 3 for the fluid names, the radio buttons
    # used in pages 4 and 5 for invalidating zero as input
    def warn_one_object(self, object_name, error_name, invalid_data=None):
        # label_name = " ".join(lineEdit_object_name.split("_")[2:]) # for instance, 'Mass flowrate'
        if object_name:
            if error_name == "ZeroInputError":
                # DoubleSpinBox_exmaple_name -> label_example_name
                label_name = "label" + object_name[13:]
            else:
                label_name = "label" + object_name[8:]
            # to handle the labels with rich text 
            if label_name == "label_Core_tube_outer_diameter":
                label_text = self.get_real_label_texts(label_name)
            elif label_name == "label_Average_spiral_diameter":
                label_text = self.get_real_label_texts(label_name)
            else:
                label = getattr(self.main_window, label_name)
                label_text = label.text()

        # PREVIOUS IMPLEMENTATION FOR LINE EDITS: FOR CHECKING THAT THERE WASN'T ANY EMPTY LINE
        if error_name == "EmptyLineError":
            console_error_text = f"{error_name}: The lineEdit '{object_name}', associated to the label '{label_name}' cannot be empty."
        elif error_name == "ZeroInputError":
            console_error_text = f"{error_name}: The double spin box '{object_name}', associated to the label '{label_name}' cannot have zero as value."
        elif error_name == "SelectionError":
            console_error_text = f"{error_name}: There's no radio button group selected for localizing the hot fluid at page 4."
            label_text = ""
        elif error_name == "ValueError":
            console_error_text = f"{error_name}: The lineEdit '{object_name}', associated to the label '{label_name}' has a invalid data."
        print(console_error_text)

        if invalid_data:
            label_text = invalid_data
            
        QMessageBox.warning(self.main_window, warnings[error_name]["title"][self.main_window.lang],
                                warnings[error_name]["text"][self.main_window.lang].format(label_text))


    # used in page 3 for the fluid names
    # used in pages 4 and 5 for invalidating zero as input
    def warn_serveral_objects(self, objects, error_name, invalid_datas=[]):                
        object_names = [o.objectName() for o in objects]
        
        # label_text = ""
        # for line_edit_name in lineEdit_object_names:
        #     label_name = "label" + line_edit_name[8:]
        #     label = getattr(self, label_name)
        #     label_text = label_text + label.text() + ", "
        # label_text = label_text[:len(label_text) - 2] # eliminate the last comma and the space
        
        # PREVIOUS IMPLEMENTATION FOR LINE EDITS: FOR CHECKING THAT THERE WASN'T ANY EMPTY LINE
        label1 = ""
        label2 = ""
        if error_name == "SeveralZeroInputsError":
            console_error_text = f"{error_name}: The doubleSpinBoxes '{object_names}', cannot be zero for the calculations."
        elif error_name == "SeveralValuesError":
            console_error_text = f"{error_name}: The lineEdits '{object_names}' have invalid datas."
        elif error_name == "SeveralEmptyLinesError":
            console_error_text = f"{error_name}: The lineEdits '{object_names}', cannot be empty."
            label1, label2 = ["label" + name[8:] for name in object_names]
            label1 = getattr(self.main_window, label1).text()
            label2 = getattr(self.main_window, label2).text()
            
        print(console_error_text)
        QMessageBox.warning(self.main_window, warnings[error_name]["title"][self.main_window.lang],
                                warnings[error_name]["text"][self.main_window.lang].format(label1, label2))


    # TESTS AND WARNINGS FOR POSSIBLE ERRORS IN PAGE 4
    # Checks if there is any zero in the page inputs, displaying a warning 
    # if so. It is used in the check_page_4_data method and in the check_page_5_data
    # methods, so it needs the argument double_spin_boxes.
    def check_zero_in_page(self, double_spin_boxes):
        
        # # the inlet and outlert temperatures of both fluids are the only parameters
        # # that can be zero
        # double_spin_boxes = all_double_spin_boxes.copy()
        # double_spin_boxes.remove(self.main_window.doubleSpinBox_hot_Inlet_temperature)
        # double_spin_boxes.remove(self.main_window.doubleSpinBox_hot_Outlet_temperature)
        # double_spin_boxes.remove(self.main_window.doubleSpinBox_cold_Inlet_temperature)
        # double_spin_boxes.remove(self.main_window.doubleSpinBox_cold_Outlet_temperature)

        count = 0
        double_spin_box_with_value_zero = []
        for double_spin_box in double_spin_boxes:
            if double_spin_box.value() == 0:
                count += 1
                double_spin_box_with_value_zero.append(double_spin_box)
                # line_edit.setStyleSheet(self.wrong_style)
            # else:
            #     line_edit.setStyleSheet(self.standard_style)
            
        if count:
            if count == 1:
                self.warn_one_object(double_spin_box_with_value_zero[0].objectName(), "ZeroInputError")
            else:
                self.warn_serveral_objects(double_spin_box_with_value_zero, "SeveralZeroInputsError")
            return False
        return True    
    
    def test_Qh_Qc_ratio(self):
        Qh = round((self.main_window.doubleSpinBox_hot_Mass_flowrate.value() * self.main_window.doubleSpinBox_hot_Specific_heat.value() * (self.main_window.doubleSpinBox_hot_Inlet_temperature.value() - self.main_window.doubleSpinBox_hot_Outlet_temperature.value())) / 3600, self.main_window.design_calculator.digits_for_rounding)
        Qc = round((self.main_window.doubleSpinBox_cold_Mass_flowrate.value() * self.main_window.doubleSpinBox_cold_Specific_heat.value() * (self.main_window.doubleSpinBox_cold_Outlet_temperature.value() - self.main_window.doubleSpinBox_cold_Inlet_temperature.value())) / 3600, self.main_window.design_calculator.digits_for_rounding)

        # debugging
        # print("Qh: ", self.Qh)
        # print("Qc: ", self.Qc)

        try:
            ratio = Qh / Qc
        except ZeroDivisionError as e:
            print(f"{e}\nRatio isn't correct. Please, check the related parameters in the previous pages (red colored).")
            ratio = warnings["ZeroDivisionError"][self.main_window.lang]
            self.warn_wrong_ratio(ratio)
            return False
        else:
            if not 1.030 > ratio > 0.970:
                ratio = round(ratio, 3)
                self.warn_wrong_ratio(ratio)
                return False

        # if the test is passed return to the original color the double spin boxes
        self.main_window.doubleSpinBox_hot_Mass_flowrate.setStyleSheet(self.standard_style)
        self.main_window.doubleSpinBox_hot_Specific_heat.setStyleSheet(self.standard_style)
        self.main_window.doubleSpinBox_hot_Inlet_temperature.setStyleSheet(self.standard_style)
        self.main_window.doubleSpinBox_hot_Outlet_temperature.setStyleSheet(self.standard_style)

        self.main_window.doubleSpinBox_cold_Mass_flowrate.setStyleSheet(self.standard_style)
        self.main_window.doubleSpinBox_cold_Specific_heat.setStyleSheet(self.standard_style)
        self.main_window.doubleSpinBox_cold_Inlet_temperature.setStyleSheet(self.standard_style)
        self.main_window.doubleSpinBox_cold_Outlet_temperature.setStyleSheet(self.standard_style)

        # and take advantage of the aready calculated ratio
        self.design_results.Qh_Qc_ratio = ratio

        return True

    def warn_wrong_ratio(self, ratio, error_name="RatioError"):
        print("Ratio hasn't a correct ratio. Please, check the related parameters (red colored).")

        # self.label_ratio_Qh_Qc.setStyleSheet(self.wrong_style)
        self.main_window.doubleSpinBox_hot_Mass_flowrate.setStyleSheet(self.wrong_style)
        self.main_window.doubleSpinBox_hot_Specific_heat.setStyleSheet(self.wrong_style)
        self.main_window.doubleSpinBox_hot_Inlet_temperature.setStyleSheet(self.wrong_style)
        self.main_window.doubleSpinBox_hot_Outlet_temperature.setStyleSheet(self.wrong_style)

        self.main_window.doubleSpinBox_cold_Mass_flowrate.setStyleSheet(self.wrong_style)
        self.main_window.doubleSpinBox_cold_Specific_heat.setStyleSheet(self.wrong_style)
        self.main_window.doubleSpinBox_cold_Inlet_temperature.setStyleSheet(self.wrong_style)
        self.main_window.doubleSpinBox_cold_Outlet_temperature.setStyleSheet(self.wrong_style)

        print(str(type(ratio)))
        if "float" in str(type(ratio)):
            text = "wrong"
            ratio = str(ratio)
        elif "str" in str(type(ratio)):
            text = "undefined"
        print(text)
        QMessageBox.warning(self.main_window, warnings[error_name]["title"][self.main_window.lang],
                                warnings[error_name][text][self.main_window.lang].format(ratio))    

    
    # used in page 5
    def test_diameters(self):

        # Dk < DH is the correct proposition
        if self.input_data.Core_tube_outer_diameter >= self.input_data.Average_spiral_diameter:
            self.warn_invalid_diameter("label_Core_tube_outer_diameter", "label_Average_spiral_diameter")
            return False
        
        # Dk < Di is the correct proposition
        if self.input_data.Core_tube_outer_diameter >= self.input_data.Shell_inner_diameter:
            self.warn_invalid_diameter("label_Core_tube_outer_diameter", "label_Shell_inner_diameter")
            return False
        
        # DH < Di is the correct proposition
        if self.input_data.Average_spiral_diameter >= self.input_data.Shell_inner_diameter:
            self.warn_invalid_diameter("label_Average_spiral_diameter", "label_Shell_inner_diameter")
            return False

        # di < do is the correct proposition
        if self.input_data.Tube_inner_diameter >= self.input_data.Tube_outer_diameter:
            self.warn_invalid_diameter("label_Tube_inner_diameter", "label_Tube_outer_diameter")
            return False
        return True

    def warn_invalid_diameter(self, label_name1, label_name2, error_name="DiameterError"):
        # I couldn't create a subscript 'K' and used HTML (for rich text). But the I didn't remember the error 
        # text displayed uses the text in the label. I couldn't come up with a better solution that this:
        text1, text2 = self.get_real_label_texts(label_name1, label_name2)

        print(f"{error_name}: diameter with labeled '{text1}' must to be greater than the diameter labeled '{text2}' for the design calculations to be correct.")

        QMessageBox.warning(self.main_window, warnings[error_name]["title"][self.main_window.lang],
                                warnings[error_name]["text"][self.main_window.lang].format(text1, text2))

    # to avoid the rich text being displayed in the message of the warning window
    def get_real_label_texts(self, label_name1, label_name2=""):
        if label_name2:
            # Dk < DH
            if label_name1 == "label_Core_tube_outer_diameter" and label_name2 == "label_Average_spiral_diameter":
                text1 = DK_DH_diameters[self.main_window.lang]["label_Core_tube_outer_diameter"] # DK
                text2 = DK_DH_diameters[self.main_window.lang]["label_Average_spiral_diameter"] # DH
            # Dk < Di (the second part is not necessary)
            elif label_name1 == "label_Core_tube_outer_diameter": # and label_name2 == "label_Shell_inner_diameter":
                text1 = DK_DH_diameters[self.main_window.lang]["label_Core_tube_outer_diameter"] # DK
                label2 = getattr(self.main_window, label_name2)
                text2 = label2.text()
            # DH < Di (same for this other)
            elif label_name1 == "label_Average_spiral_diameter": # and label_name2 == "label_Shell_inner_diameter":
                text1 = DK_DH_diameters[self.main_window.lang]["label_Average_spiral_diameter"] # DH
                label2 = getattr(self.main_window, label_name2)
                text2 = label2.text()
            else:
                label1 = getattr(self.main_window, label_name1)
                label2 = getattr(self.main_window, label_name2)
                text1 = label1.text()
                text2 = label2.text()
            return text1, text2
        else:
            if label_name1 == "label_Core_tube_outer_diameter": # Dk
                text1 = DK_DH_diameters[self.main_window.lang]["label_Core_tube_outer_diameter"]
            elif label_name1 == "label_Average_spiral_diameter": # DH
                text1 = DK_DH_diameters[self.main_window.lang]["label_Average_spiral_diameter"]
            else:
                label1 = getattr(self.main_window, label_name1)
                text1 = label1.text()
            return text1
            

    def test_coil_Reynolds_number(self):
        # in order to test that the Reynolds number of the coil and shell-side fluids is correct
        # we need to proceed with the necessary calculations
        self.design_calculator.calculate_page_6()
        result = self.design_results.coil_Nusselt_number
        if result in [-1, None]:
            self.warn_not_supported_Reynolds(result, "coil")
            return False
        # set all the styles back to normal
        try:
            for parameter in self.parameters_for_coloring:
                parameter.setStyleSheet(self.standard_style)
        except AttributeError as e:
            print(e)
        return True
    
    def test_shell_Reynolds_number(self):
        # PREVIOUS INNEFFICIENT IMPLEMENTATION
        # outer_spiral_diameter = self.design_calculator.outer_spiral_diameter(self.input_data.Shell_inner_diameter, self.input_data.Tube_outer_diameter)
        # inner_spiral_diameter = self.design_calculator.inner_spiral_diameter(self.input_data.Core_tube_outer_diameter, self.input_data.Tube_outer_diameter)
        # shell_flow_cross_section = self.design_calculator.shell_flow_cross_section(self.input_data.Shell_inner_diameter, self.input_data.Core_tube_outer_diameter, outer_spiral_diameter, inner_spiral_diameter)
        # shell_volumetric_flowrate = self.design_calculator.shell_volumetric_flowrate(self.input_data.shell_Mass_flowrate, self.input_data.shell_Density)
        # shell_velocity = self.design_calculator.shell_velocity(shell_volumetric_flowrate, shell_flow_cross_section)
        # length_coil_needed = self.design_calculator.length_coil_needed(self.input_data.Average_spiral_diameter, self.input_data.Tube_pitch)
        # volume_occupied_by_coil = self.design_calculator(self.input_data.Tube_outer_diameter, length_coil_needed)
        # volume_of_shell = self.design_calculator.volume_of_shell(self.input_data.Shell_inner_diameter, self.input_data.Core_tube_outer_diameter, self.input_data.Tube_pitch)
        # volume_available_flow_shell = self.design_calculator.volume_available_flow_shell(volume_of_shell, volume_occupied_by_coil)
        # equivalent_diameter = self.design_calculator.equivalent_diameter(volume_available_flow_shell, self.input_data.tube_outer_diameter, length_coil_needed)
        # shell_Reynolds_number = self.design_calculator.shell_Reynolds_number(equivalent_diameter, shell_velocity, self.input_data.shell_Density, self.input_data.shell_Viscosity)
        # shell_Prandtl_number = self.design_calculator.shell_Prandtl_number(self.input_data.shell_Specific_heat, self.input_data.shell_Viscosity, self.input_data.shell_Thermal_conductivity)
        # shell_heat_transfer_coeficient = self.design_calculator.shell_heat_transfer_coeficient(shell_Reynolds_number, self.input_data.shell_Thermal_conductivity, equivalent_diameter, shell_Prandtl_number)

        self.design_calculator.calculate_page_6()
        result = self.design_results.shell_heat_transfer_coeficient
        if result in [-1, None]:
            self.warn_not_supported_Reynolds(result, "shell")
            return False
        # set all the styles that were colored red (in the method 'warn_not_supported_Reynolds') back to normal
        try:
            for parameter in self.parameters_for_coloring:
                parameter.setStyleSheet(self.standard_style)
        except AttributeError as e:
            print(e)
        return True

    def warn_not_supported_Reynolds(self, value, location, error_name="ReynoldsError"):
        print(f"This software does not support the value '{value}' for the Reynolds number. Please, check the related parameters (red colored).")

        # if the location of the Reynolds number value out of the supported range is in the coil
        if location == "coil": # which means the value is < 2300
            # parameters needed for the calculation of the Reynolds number in coil
            if self.input_data.hot_in_shell:
                self.parameters_for_coloring = [self.main_window.doubleSpinBox_cold_Mass_flowrate, self.main_window.doubleSpinBox_cold_Density, self.main_window.doubleSpinBox_Tube_inner_diameter, self.main_window.doubleSpinBox_cold_Viscosity]
            elif self.input_data.hot_in_coil:
                self.parameters_for_coloring = [self.main_window.doubleSpinBox_hot_Mass_flowrate, self.main_window.doubleSpinBox_hot_Density, self.main_window.doubleSpinBox_Tube_inner_diameter, self.main_window.doubleSpinBox_hot_Viscosity]
        
        # still don't know if the value of shell_Reynolds_number can cause an error
        elif location == "shell": # which means the value is < 50
            if self.input_data.hot_in_shell:
                individual_ones = [self.main_window.doubleSpinBox_hot_Thermal_conductivity, self.main_window.doubleSpinBox_hot_Mass_flowrate, self.main_window.doubleSpinBox_hot_Density, self.main_window.doubleSpinBox_hot_Viscosity, self.main_window.doubleSpinBox_hot_Specific_heat]
            elif self.input_data.hot_in_coil:
                individual_ones = [self.main_window.doubleSpinBox_cold_Thermal_conductivity, self.main_window.doubleSpinBox_cold_Mass_flowrate, self.main_window.doubleSpinBox_cold_Density, self.main_window.doubleSpinBox_cold_Viscosity, self.main_window.doubleSpinBox_cold_Specific_heat]
            common_for_both = [self.main_window.doubleSpinBox_Tube_outer_diameter, self.main_window.doubleSpinBox_Tube_pitch, self.main_window.doubleSpinBox_Shell_inner_diameter, self.main_window.doubleSpinBox_Core_tube_outer_diameter, self.main_window.doubleSpinBox_Average_spiral_diameter]
            self.parameters_for_coloring = individual_ones + common_for_both
        # for a better explaination refer to: "block diagram - hot fluid in coil 3.0.png" or "block diagram - hot fluid in shell 3.0.png"

        for parameter in self.parameters_for_coloring:
            parameter.setStyleSheet(self.wrong_style)

        QMessageBox.warning(self.main_window, warnings[error_name][location]["title"][self.main_window.lang],
                                warnings[error_name][location]["text"][self.main_window.lang])
        
    def warn_incorrect_input(self, error_name="IncorrectInput", parameter_label_name="", result=0):
        if not parameter_label_name and not result:
            QMessageBox.warning(self.main_window, warnings[error_name]["title"][self.main_window.lang],
                                warnings[error_name]["text"][self.main_window.lang])
        elif parameter_label_name == "label_6_table0_0":
            parameter_label_text = self.main_window.label_6_table0_0.text()
            related_input_label_text = self.main_window.label_Tube_inner_diameter.text()
            self.main_window.doubleSpinBox_Tube_inner_diameter.setStyleSheet(self.wrong_style)
            QMessageBox.warning(self.main_window, warnings[error_name]["title"][self.main_window.lang],
                                warnings[error_name]["text_with_label_and_value"][self.main_window.lang].format(parameter_label_text, result, related_input_label_text))
        elif parameter_label_name == "label_7_3":
            parameter_label_text = self.main_window.label_7_3.text()
            related_input_label_texts = [self.main_window.label_hot_Inlet_temperature.text(),
                                         self.main_window.label_hot_Outlet_temperature.text(),
                                         self.main_window.label_cold_Inlet_temperature.text(),
                                         self.main_window.label_cold_Outlet_temperature.text()]
            # related_input_label_text = ", ".join(related_input_label_texts)
            self.double_spins_to_color = [self.main_window.doubleSpinBox_hot_Inlet_temperature, self.main_window.doubleSpinBox_hot_Outlet_temperature, self.main_window.doubleSpinBox_cold_Inlet_temperature, self.main_window.doubleSpinBox_cold_Outlet_temperature]
            for double_spin in self.double_spins_to_color:
                double_spin.setStyleSheet(self.wrong_style)
            if result == 'math domain error':
                QMessageBox.warning(self.main_window, warnings[error_name]["title"][self.main_window.lang],
                                    warnings[error_name]["text_LogError"][self.main_window.lang].format(parameter_label_text, related_input_label_texts[0], related_input_label_texts[1], related_input_label_texts[2], related_input_label_texts[3]))
            if result == 'division by zero':
                QMessageBox.warning(self.main_window, warnings[error_name]["title"][self.main_window.lang],
                                    warnings[error_name]["text_ZeroDivisionError"][self.main_window.lang].format(parameter_label_text, related_input_label_texts[0], related_input_label_texts[1], related_input_label_texts[2], related_input_label_texts[3]))


    # added Friday, June 7th to handle the very small values of 'tube inner diameter'. The design_calculator.cross_sectional_coil_area()
    # method with a small number as input can provide in 0 as output since the round() built-in function is used.
    def test_cross_sectional_coil_area(self):
        print("self.design_calculator.data.Tube_inner_diameter", self.design_calculator.data.Tube_inner_diameter)
        print("self.main_window.doubleSpinBox_Tube_inner_diameter.value()", self.main_window.doubleSpinBox_Tube_inner_diameter.value())
        result = self.design_calculator.cross_sectional_coil_area(self.main_window.doubleSpinBox_Tube_inner_diameter.value())
        # self.design_calculator.calculate_page_6()
        if result == 0:
            # 'label_6_table0_0' is the label of the cross_sectional_coil_area
            self.warn_incorrect_input("IncorrectInput", "label_6_table0_0", int(result))
            return False
        # set the styles back to normal
        self.main_window.doubleSpinBox_Tube_inner_diameter.setStyleSheet(self.standard_style)
        return True

    # added Friday, June 7th to handle logarithms with arguments <= 0 in the DesignCalculator method
    # log_mean_temp_difference()
    def test_log_mean_temp_difference(self):
        print("self.main_window.doubleSpinBox_hot_Inlet_temperature.value(), self.main_window.doubleSpinBox_cold_Outlet_temperature.value(), self.main_window.doubleSpinBox_hot_Outlet_temperature.value(), self.main_window.doubleSpinBox_cold_Inlet_temperature.value()", self.main_window.doubleSpinBox_hot_Inlet_temperature.value(), self.main_window.doubleSpinBox_cold_Outlet_temperature.value(), self.main_window.doubleSpinBox_hot_Outlet_temperature.value(), self.main_window.doubleSpinBox_cold_Inlet_temperature.value())
        result = self.design_calculator.log_mean_temp_difference(self.main_window.doubleSpinBox_hot_Inlet_temperature.value(), self.main_window.doubleSpinBox_cold_Outlet_temperature.value(), self.main_window.doubleSpinBox_hot_Outlet_temperature.value(), self.main_window.doubleSpinBox_cold_Inlet_temperature.value())
        if 'math domain error' in str(result):
            self.warn_incorrect_input("IncorrectInput", "label_7_3", str(result))
            return False
        if 'division by zero' in str(result):
            self.warn_incorrect_input("IncorrectInput", "label_7_3", str(result))
            return False
        # set all the styles back to normal
        try:
            for double_spin in self.double_spins_to_color:
                double_spin.setStyleSheet(self.standard_style)
        except Exception as e:
            print(e)
        return True
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QDoubleSpinBox #, QGraphicsDropShadowEffect
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon

# from time import sleep

from .dict import es, en, pressure_drop_comparisons_texts 
# from .utils import substraction_with_decimals
from .widget_for_table import Table1Widget, Table2Widget
from .input_data import InputData
from .error_handler import ErrorHandler
from .design_calculator import DesignCalculator
from .output_data import OutputData

class MainWindow(QMainWindow):
    def __init__(self): # presentation
        # self.__presentador = presentador
        QMainWindow.__init__(self)
        loadUi("resources/views/ui/main.ui", self)

        self.setWindowTitle('HeliCalc')
        self.setWindowIcon(QIcon('helical_coil_hex.jpg'))

        # ZERO PAGE
        self.label_0_pic_0.setStyleSheet("""
        border-image:url('./resources/views/assets/helical_coil_0.jpg');
        """)
        self.label_0_pic_1.setStyleSheet("""
        border-image:url('./resources/views/assets/logo_univ.svg');
        """)
        self.label_0_pic_2.setStyleSheet("""
        border-image:url('./resources/views/assets/helical_coil_1.jpg');
        """)

        self.pushButton_exit.clicked.connect(self.close)

        # it appears that ...
        self.lang = "es"
        button_es = getattr(self, "pushButton_es")
        button_en = getattr(self, "pushButton_en")
        button_es.clicked.connect(lambda _, lang="es": self.set_lang(lang))
        button_en.clicked.connect(lambda _, lang="en": self.set_lang(lang))

        # all pages except zero
        next_buttons = []
        for i in range(1, 8):
            button_next_name = f"pushButton_next_{i}"
            button_next = getattr(self, button_next_name)
            button_prev_name = f"pushButton_previous_{i}"
            button_prev = getattr(self, button_prev_name)
            button_next.clicked.connect(lambda _, page_index=i: self.goto_next_widget(page_index))
            button_prev.clicked.connect(lambda _, page_index=i: self.goto_previous_widget(page_index))
            next_buttons.append(button_next)

        button_prev_name = f"pushButton_previous_{i+1}"
        button_prev = getattr(self, button_prev_name)
        button_prev.clicked.connect(lambda _, page_index=i: self.goto_previous_widget(page_index))

        # SECOND PAGE
        self.label_intro_image_02.setStyleSheet("""
        border-image:url('./resources/views/assets/helical_coil_page_02.png');
        """)

        # THIRD PAGE 
        self.input_data = InputData()
        self.design_results = OutputData()
        self.design_calculator = DesignCalculator(self, 7)
        self.error_handler = ErrorHandler(self)
    
        # FOURTH PAGE
        self.double_spin_boxes_page_4 = [self.doubleSpinBox_hot_Mass_flowrate, self.doubleSpinBox_hot_Inlet_temperature, self.doubleSpinBox_hot_Outlet_temperature, self.doubleSpinBox_hot_Fouling_factor, self.doubleSpinBox_hot_Allowable_pressure_drop, self.doubleSpinBox_hot_Density, self.doubleSpinBox_hot_Viscosity, self.doubleSpinBox_hot_Specific_heat, self.doubleSpinBox_hot_Thermal_conductivity, self.doubleSpinBox_cold_Mass_flowrate, self.doubleSpinBox_cold_Inlet_temperature, self.doubleSpinBox_cold_Outlet_temperature, self.doubleSpinBox_cold_Fouling_factor, self.doubleSpinBox_cold_Allowable_pressure_drop, self.doubleSpinBox_cold_Density, self.doubleSpinBox_cold_Viscosity, self.doubleSpinBox_cold_Specific_heat, self.doubleSpinBox_cold_Thermal_conductivity]
        self.double_spin_boxes_page_4_without_temperatures = [self.doubleSpinBox_hot_Mass_flowrate, self.doubleSpinBox_hot_Fouling_factor, self.doubleSpinBox_hot_Allowable_pressure_drop, self.doubleSpinBox_hot_Density, self.doubleSpinBox_hot_Viscosity, self.doubleSpinBox_hot_Specific_heat, self.doubleSpinBox_hot_Thermal_conductivity, self.doubleSpinBox_cold_Mass_flowrate, self.doubleSpinBox_cold_Fouling_factor, self.doubleSpinBox_cold_Allowable_pressure_drop, self.doubleSpinBox_cold_Density, self.doubleSpinBox_cold_Viscosity, self.doubleSpinBox_cold_Specific_heat, self.doubleSpinBox_cold_Thermal_conductivity]

        self.table_1_widget = Table1Widget()
        self.pushButton0_table_1.clicked.connect(self.show_table_1)
        self.pushButton1_table_1.clicked.connect(self.show_table_1)
        # self.table_1_widget.table1_widget.cellClicked.connect(self.on_cell_clicked_table_1_widget)
        # print(self.table_1_widget.table1_widget.objectName())

        self.doubleSpinBox_hot_Inlet_temperature.textChanged.connect(lambda _, double_spin_box1=self.doubleSpinBox_hot_Inlet_temperature, double_spin_box2=self.doubleSpinBox_hot_Outlet_temperature, label=self.label_hot_Average_temperature: self.calculate_mean(double_spin_box1, double_spin_box2, label))
        self.doubleSpinBox_hot_Outlet_temperature.textChanged.connect(lambda _, double_spin_box1=self.doubleSpinBox_hot_Inlet_temperature, double_spin_box2=self.doubleSpinBox_hot_Outlet_temperature, label=self.label_hot_Average_temperature: self.calculate_mean(double_spin_box1, double_spin_box2, label))

        self.doubleSpinBox_cold_Inlet_temperature.textChanged.connect(lambda _, double_spin_box1=self.doubleSpinBox_cold_Inlet_temperature, double_spin_box2=self.doubleSpinBox_cold_Outlet_temperature, label=self.label_cold_Average_temperature: self.calculate_mean(double_spin_box1, double_spin_box2, label))
        self.doubleSpinBox_cold_Outlet_temperature.textChanged.connect(lambda _, double_spin_box1=self.doubleSpinBox_cold_Inlet_temperature, double_spin_box2=self.doubleSpinBox_cold_Outlet_temperature, label=self.label_cold_Average_temperature: self.calculate_mean(double_spin_box1, double_spin_box2, label))


        # FIFTH PAGE
        self.double_spin_boxes_page_5 = [self.doubleSpinBox_Shell_inner_diameter, self.doubleSpinBox_Core_tube_outer_diameter, self.doubleSpinBox_Average_spiral_diameter, self.doubleSpinBox_Tube_outer_diameter, self.doubleSpinBox_Tube_inner_diameter, self.doubleSpinBox_Tube_pitch, self.doubleSpinBox_Thermal_conductivity_coil_material]

        self.label_helical_coil_cross_section_page_05.setStyleSheet("""
        border-image:url('./resources/views/assets/label_helical_coil_cross_section_page_05.png');
        """)
        self.table_2_widget = Table2Widget()
        self.pushButton0_table_2.clicked.connect(self.show_table_2)
        # self.table_2_widget.cellClicked.connect(self.table_2_widget.on_cell_clicked)

        # SIXTH PAGE
        # self.design_results = self.design_calculator.results

        # SEVENTH PAGE
        self.doubleSpinBox_Temperature_correction_factor.setValue(self.input_data.Temperature_correction_factor)
        self.doubleSpinBox_Temperature_correction_factor.textChanged.connect(self.load_page_7_results)

        # EIGTH PAGE
        self.doubleSpinBox_coil_Isentropic_efficiency_pump.setValue(self.input_data.coil_Isentropic_efficiency_pump)
        self.doubleSpinBox_coil_Isentropic_efficiency_pump.textChanged.connect(self.load_page_8_results)

        self.doubleSpinBox_shell_Isentropic_efficiency_pump.setValue(self.input_data.shell_Isentropic_efficiency_pump)
        self.doubleSpinBox_shell_Isentropic_efficiency_pump.textChanged.connect(self.load_page_8_results)

        self.pushButton_restart.clicked.connect(self.reset)

    # FUNCTIONALITIES FOR PAGE 0
    def set_lang(self, lang):
        self.lang = lang
        if lang == "es":
            for k in es.keys():
                item = getattr(self, k)
                item.setText(es[k])            
        elif lang == "en":
            for k in en.keys():
                item = getattr(self, k)
                item.setText(en[k])
        self.goto_next_widget(0) # go to the page number one

    # FUNCTIONALITIES FOR VARIOUS PAGES, including page 1
    def goto_next_widget(self, page_index):
        if page_index == 3:
            if not self.check_page_3_data():
                return
        elif page_index == 4:
            if not self.check_page_4_data():
                return
        elif page_index == 5:
            if not self.check_page_5_data():
                return
            print("\n\nPage 6 loaded althouth it shouldn't")
            self.load_page_6_results()
            self.load_page_7_results()
            self.load_page_8_results()
        self.stackedWidget.setCurrentIndex(page_index + 1)

    def goto_previous_widget(self, page_index):
       self.stackedWidget.setCurrentIndex(page_index - 1)

    # FUNCTINALITIES FOR PAGE 3              
    # Checks all the data in the page 3 was entered: the name of the two
    # fluids and the location of the hot fluid. It uses fluids_names_entered
    # and radioButton_selected for raising errors (displaying a window with 
    # QMessageBox.warning()). It also calls store_page_3_data and 
    # set_dynamic_text, and set the default color of the labels of the fluid names.
    def check_page_3_data(self):
        entered = self.error_handler.check_fluids_names()
        if not entered:
            return False
        selected = self.error_handler.test_radio_button_selected()
        if not selected:
            return False
        self.store_page_3_data()
        self.set_dynamic_text()
        return True

    def store_page_3_data(self):
        # store the radio button selection
        selected = self.buttonGroup.checkedButton()
        text = selected.text()
        print("selected.text()", selected.text())
        print("text in [Shell, Coraza]", text in ["Shell", "Coraza"])
        print("text in [Coil, Serpentín]", text in ["Coil", "Serpentín"])
        print("before self.input_data.hot_in_shell", self.input_data.hot_in_shell)
        print("before self.input_data.hot_in_coil", self.input_data.hot_in_coil)
        if text in ["Shell", "Coraza"]:
            self.input_data.hot_in_shell = True
            self.design_results.hot_in_shell = True
            self.input_data.hot_in_coil = False
            self.design_results.hot_in_coil = False
        if text in ["Coil ", "Serpentín"]: # The sapce in "Coil " is NEEDED!!!
            self.input_data.hot_in_shell = False
            self.design_results.hot_in_shell = False
            self.input_data.hot_in_coil = True
            self.design_results.hot_in_coil = True
        print("after self.input_data.hot_in_shell", self.input_data.hot_in_shell)
        print("after self.input_data.hot_in_coil", self.input_data.hot_in_coil)

        # store the names of the fluids
        self.input_data.hot_fluid_name = self.lineEdit_Name_hot_fluid.text()
        self.input_data.cold_fluid_name = self.lineEdit_Name_cold_fluid.text()

        # set the label's texts of the next page
        self.label_4_hot_name.setText(self.input_data.hot_fluid_name)
        self.label_4_cold_name.setText(self.input_data.cold_fluid_name)

    # make some label texts change dynamically according to the selection
    # of the radio buttons
    # 7. Fix error: "coil, serpentin, shell, coraza" texts aren't changing properly
    def set_dynamic_text(self):
        if self.lang == "es":
            if self.input_data.hot_in_shell:
                shell = "caliente"
                coil = "frío"
            elif self.input_data.hot_in_coil:
                shell = "frío"
                coil = "caliente"
            item = getattr(self, "label_6_1_coil")
            item.setText("Fluido {0} (serpentín)".format(coil))

            item = getattr(self, "label_6_3_shell")
            item.setText("Fluido {0} (coraza)".format(shell))

            item = getattr(self, "label_6_2_coil")
            item.setText("Carga de calor (Q{0})".format("c" if coil=="frío" else "h"))
            item = getattr(self, "label_6_4_shell")
            item.setText("Carga de calor (Q{0})".format("c" if shell=="frío" else "h"))

            item = getattr(self, "label_8_1_coil")
            item.setText("Fluido {0} (serpentín)".format(coil))
            item = getattr(self, "label_8_5_shell")
            item.setText("Fluido {0} (coraza)".format(shell))

            item = getattr(self, "label_8_9_coil")
            item.setText("Fluido {0} (serpentín)".format(coil))
            item = getattr(self, "label_8_12_shell")
            item.setText("Fluido {0} (coraza)".format(shell))

        elif self.lang == "en":
            if self.input_data.hot_in_shell:
                shell = "Hot"
                coil = "Cold"
            elif self.input_data.hot_in_coil:
                shell = "Cold"
                coil = "Hot"

            item = getattr(self, "label_6_1_coil")
            item.setText("{0} fluid (coil)".format(coil))

            item = getattr(self, "label_6_3_shell")
            item.setText("{0} fluid (shell)".format(shell))

            item = getattr(self, "label_6_2_coil")
            item.setText("Heat load (Q{0})".format("c" if coil=="Cold" else "h"))
            item = getattr(self, "label_6_4_shell")
            item.setText("Heat load (Q{0})".format("c" if shell=="Cold" else "h"))

            item = getattr(self, "label_8_1_coil")
            item.setText("{0} fluid (coil)".format(coil))
            item = getattr(self, "label_8_5_shell")
            item.setText("{0} fluid (shell)".format(shell))

            item = getattr(self, "label_8_9_coil")
            item.setText("{0} fluid (coil)".format(coil))
            item = getattr(self, "label_8_12_shell")
            item.setText("{0} fluid (shell)".format(shell))

    # FUNCTIONALITIES FOR PAGE 4
    def show_table_1(self):
        # for creating a new table every time the button is clicked
        if self.table_1_widget:
            self.table_1_widget = Table1Widget(self.lang)
            self.table_1_widget.show()

    def calculate_mean(self, double_spin_box1, double_spin_box2, label):
        try:
            hot_in = float(double_spin_box1.value())
            hot_out = float(double_spin_box2.value())
        except ValueError as e:
            print(e)
        except Exception as unecpected_err:
            print(unecpected_err)
        else:
            mean = (hot_in + hot_out) / 2
            label.setText(str(mean))

    # Check all the double spin boxes have correct values. This includes:
    # (i) none of them can have zero as value,
    # (ii) the ratio of the heat loads of the hot and cold fluids (Qh/Qc ratio) must be between 1.030 and 0.970,
    # (iii) store the input data of the page for the design calculations
    def check_page_4_data(self):
        correct = self.error_handler.check_zero_in_page(self.double_spin_boxes_page_4_without_temperatures)
        if not correct:
            return False
        
        correct = self.error_handler.test_Qh_Qc_ratio()
        if not correct:
            return False
        
        valid_log = self.error_handler.test_log_mean_temp_difference()
        if not valid_log:
            return False

        self.store_page_data(self.double_spin_boxes_page_4)

        return True

    def store_page_data(self, double_spin_boxes):
        for double_spin_box in double_spin_boxes:
            object_name = double_spin_box.objectName()
            parameter_name = object_name[14:]
            setattr(self.input_data, parameter_name, double_spin_box.value())

    # FUNCTIONALITIES FOR PAGE 5
    def show_table_2(self):
        # for creating a new table every time the button is clicked
        if self.table_2_widget:
            self.table_2_widget = Table2Widget(self.lang)
            self.table_2_widget.show()
        
    def check_page_5_data(self):

        if not self.error_handler.check_zero_in_page(self.double_spin_boxes_page_5):
            return False

        # we store the input data of the page to be able to access it
        # from the InputData object, specifically inside the ErrorHandler
        self.store_page_data(self.double_spin_boxes_page_5)
        
        correct_diameters = self.error_handler.test_diameters()
        if not correct_diameters:
            return False
        
        correct_area = self.error_handler.test_cross_sectional_coil_area()
        if not correct_area:
            return

        correct_coil_Reynolds = self.error_handler.test_coil_Reynolds_number()
        if not correct_coil_Reynolds:
            return False

        correct_shell_Reynolds = self.error_handler.test_shell_Reynolds_number()
        if not correct_shell_Reynolds:
            return False

        return True


    # FUNCTIONALITIES FOR PAGE 6
    # calculate the results for pages 6, 7 and 8
    def load_page_6_results(self):
        # since the ErrorHanlder class needs to call DesignCalculator.calculate_page_6() method
        # in order to make sure the Reynolds number is in the correct range for the coil-side fluid
        # and for the shell-side fluid, we do not call again that method to avoid the same calculation
        # (take into account that the calculate_page_6() method also stores al the results in the 
        # OuputData object).

        # dictionary with the structure: key -> label for setting the results, 
                                        # value -> tuple  with result at index 0, and the number of digits to round the result at index 1
        self.page_6_labels_values_round_digits = {self.label_ratio_Qh_Qc: (self.design_results.Qh_Qc_ratio, 3), self.label_coil_Heat_load: (self.design_results.coil_heat_load, 3), self.label_shell_Heat_load: (self.design_results.shell_heat_laod, 3), self.label_Average_heat_load: (self.design_results.average_heat_load, 3), self.label_coil_Cross_sectional_area: (self.design_results.cross_sectional_coil_area, 6), self.label_coil_Volumetric_flowrate: (self.design_results.coil_volumetric_flowrate, 6), self.label_coil_Velocity: (self.design_results.coil_velocity, 3), self.label_coil_Reynolds_number: (self.design_results.coil_Reynolds_number, 2), self.label_coil_Prandtl_number: (self.design_results.coil_Prandtl_number, 3), self.label_coil_Nusselt_number: (self.design_results.coil_Nusselt_number, 2), self.label_coil_Heat_transfer_coefficient: (self.design_results.coil_heat_transfer_coeficient, 2), self.label_coil_Heat_transfer_coeficient_inside: (self.design_results.coil_heat_transfer_coeficient_inside_diameter, 2), self.label_coil_Heat_transfer_coeficient_outside: (self.design_results.coil_heat_transfer_coeficient_outside_diameter, 2), self.label_Outer_spiral_diameter: (self.design_results.outer_spiral_diameter, 4), self.label_Inner_spiral_diameter: (self.design_results.inner_spiral_diameter, 4), self.label_shell_flow_cross_section: (self.design_results.shell_flow_cross_section, 4), self.label_shell_Volumetric_flowrate: (self.design_results.shell_volumetric_flowrate, 6), self.label_shell_Velocity: (self.design_results.shell_velocity, 5), self.label_length_coil_needed: (self.design_results.length_coil_needed, 3), self.label_Volume_occupied_coil: (self.design_results.volume_occupied_by_coil, 5), self.label_Volume_shell: (self.design_results.volume_of_shell, 5), self.label_Volume_available_flow_in_shell: (self.design_results.volume_available_flow_shell, 5), self.label_Equivalent_diameter: (self.design_results.equivalent_diameter, 4), self.label_shell_Reynolds_number: (self.design_results.shell_Reynolds_number, 3), self.label_shell_Prandtl_number: (self.design_results.shell_Prandtl_number, 3), self.label_shell_Heat_transfer_coeficient: (self.design_results.shell_heat_transfer_coeficient, 2)}

        self.set_resutls_in_labels(self.page_6_labels_values_round_digits)

    # for setting the results in their labels with the corresponding digits to round
    def set_resutls_in_labels(self, labels_values_digits_dictionary):
        print("debugging set_resutls_in_labels() method:")
        for label, values in labels_values_digits_dictionary.items():
            print("label", label.text())
            print("values", values)
            label.setText(str(round(values[0], values[1])))
            print()

    # calculations of the page 7
    def load_page_7_results(self):
        self.input_data.Temperature_correction_factor = self.doubleSpinBox_Temperature_correction_factor.value()
        self.design_calculator.calculate_page_7()
        # set the results in their labels

        self.page_7_labels_values_round_digits = {self.label_Coil_wall_thickness: (self.design_results.coil_wall_thickness, 5), self.label_Overall_heat_transfer_coeficient: (self.design_results.overall_heat_transfer_coeficient, 2), self.label_Log_mean_temperature_difference: (self.design_results.log_mean_temp_difference, 2), self.label_Effective_mean_temperature_difference: (self.design_results.effective_mean_temperature_difference, 2), self.label_Spiral_total_surface_area: (self.design_results.spiral_total_surface_area, 2), self.label_Numbers_turns_coil: (self.design_results.number_of_turns_coil, 0), self.label_Calculated_spiral_tube_length: (self.design_results.calculated_spiral_total_tube_length, 2), self.label_Height_of_cylinder: (self.design_results.height_of_cylinder, 2)}
        self.set_resutls_in_labels(self.page_7_labels_values_round_digits)

    # calculations for the page 8
    def load_page_8_results(self):

        self.input_data.coil_Isentropic_efficiency_pump = self.doubleSpinBox_coil_Isentropic_efficiency_pump.value()
        self.input_data.shell_Isentropic_efficiency_pump = self.doubleSpinBox_shell_Isentropic_efficiency_pump.value()
        self.design_calculator.calculate_page_8()
        # set the results in their labels
        self.page_8_labels_values_round_digits = {self.label_coil_Factor_E: (self.design_results.coil_Factor_E, 4), self.label_coil_Friction_factor: (self.design_results.coil_Friction_factor, 4), self.label_coil_Pressure_drop: (self.design_results.coil_Pressure_drop, 2), self.label_shell_Drag_coeficient: (self.design_results.shell_drag_coeficient, 4), self.label_shell_Pressure_drop: (self.design_results.shell_Pressure_drop, 4), self.label_coil_Pumping_power: (self.design_results.coil_Pumping_power, 4), self.label_shell_Pumping_power: (self.design_results.shell_Pumping_power, 6)}
        self.set_resutls_in_labels(self.page_8_labels_values_round_digits)
        self.set_dynamic_labels_texts()
        self.stick_out_labels()

    # change labels color
    def stick_out_labels(self):
        self.timer = QTimer()
        self.have_black_color = True
        self.timer.timeout.connect(self.change_label_color)
        self.timer.start(500)

    def set_dynamic_labels_texts(self):

        # set the hover hints for the labels
        self.label_Comparison_coil_page_8.setToolTip(pressure_drop_comparisons_texts["hover_text"][self.lang])
        self.label_Comparison_shell_page_8.setToolTip(pressure_drop_comparisons_texts["hover_text"][self.lang])

        # also set pointing hand cursors for them
        self.label_Comparison_coil_page_8.setCursor(Qt.PointingHandCursor)
        self.label_Comparison_shell_page_8.setCursor(Qt.PointingHandCursor)

    def set_resulting_color(self):
        # get the comparison results
        comparison_results = self.design_calculator.get_comprarison_pressure_values()

        # if the coil pressure drop is correct we set it a text to indicate the correct results (a green colored text)
        if comparison_results["coil"]:
            self.label_Comparison_coil_page_8.setText(pressure_drop_comparisons_texts["green_colored"][self.lang])
            
            # change color
            self.set_green_color_to(self.label_Comparison_coil_page_8)        
        # otherwise we set a text to indicate the incorrect result (a red colored one)
        else:
            self.label_Comparison_coil_page_8.setText(pressure_drop_comparisons_texts["red_colored"][self.lang])
            
            # change color
            self.set_red_color_to(self.label_Comparison_coil_page_8)

        # same for the shell
        if comparison_results["shell"]:
            self.label_Comparison_shell_page_8.setText(pressure_drop_comparisons_texts["green_colored"][self.lang])
            
            # change color
            self.set_green_color_to(self.label_Comparison_shell_page_8)
        else:
            self.label_Comparison_shell_page_8.setText(pressure_drop_comparisons_texts["red_colored"][self.lang])
            
            # change color
            self.set_red_color_to(self.label_Comparison_shell_page_8)

    def change_label_color(self):
        if self.have_black_color:
            self.set_resulting_color()
            self.have_black_color = False
        else:
            self.set_black_color_to(self.label_Comparison_coil_page_8)
            self.set_black_color_to(self.label_Comparison_shell_page_8)
            self.have_black_color = True

    def set_green_color_to(self, label):
        label.setStyleSheet("""color: rgb(0, 255, 0);""")
    
    def set_red_color_to(self, label):
        label.setStyleSheet("""color: rgb(255, 62, 62);""")

    def set_black_color_to(self, label):
        label.setStyleSheet("""color: rgb(0, 0, 0);""")

    def reset(self):
        page3 = [self.lineEdit_Name_hot_fluid, self.lineEdit_Name_cold_fluid]

        # these two were eliminated from page 4: self.label_hot_Average_temperature, self.label_cold_Average_temperature,
        page4 = [self.doubleSpinBox_hot_Mass_flowrate, self.doubleSpinBox_hot_Inlet_temperature, self.doubleSpinBox_hot_Outlet_temperature, self.doubleSpinBox_hot_Fouling_factor, self.doubleSpinBox_hot_Allowable_pressure_drop, self.doubleSpinBox_hot_Density, self.doubleSpinBox_hot_Viscosity, self.doubleSpinBox_hot_Specific_heat, self.doubleSpinBox_hot_Thermal_conductivity, self.doubleSpinBox_cold_Mass_flowrate, self.doubleSpinBox_cold_Inlet_temperature, self.doubleSpinBox_cold_Outlet_temperature, self.doubleSpinBox_cold_Fouling_factor, self.doubleSpinBox_cold_Allowable_pressure_drop, self.doubleSpinBox_cold_Density, self.doubleSpinBox_cold_Viscosity, self.doubleSpinBox_cold_Specific_heat, self.doubleSpinBox_cold_Thermal_conductivity]
        page5 = [self.doubleSpinBox_Shell_inner_diameter, self.doubleSpinBox_Core_tube_outer_diameter, self.doubleSpinBox_Average_spiral_diameter, self.doubleSpinBox_Tube_outer_diameter, self.doubleSpinBox_Tube_inner_diameter, self.doubleSpinBox_Tube_pitch, self.doubleSpinBox_Thermal_conductivity_coil_material]
        page6 = [self.label_coil_Heat_load, self.label_shell_Heat_load, self.label_Average_heat_load, self.label_coil_Cross_sectional_area, self.label_coil_Volumetric_flowrate, self.label_coil_Velocity, self.label_coil_Reynolds_number, self.label_coil_Prandtl_number, self.label_coil_Nusselt_number, self.label_coil_Heat_transfer_coefficient, self.label_coil_Heat_transfer_coeficient_inside, self.label_coil_Heat_transfer_coeficient_outside, self.label_Outer_spiral_diameter, self.label_Inner_spiral_diameter, self.label_shell_flow_cross_section, self.label_shell_Volumetric_flowrate, self.label_shell_Velocity, self.label_length_coil_needed, self.label_Volume_shell, self.label_Volume_available_flow_in_shell, self.label_Equivalent_diameter, self.label_shell_Reynolds_number, self.label_shell_Prandtl_number, self.label_shell_Heat_transfer_coeficient]
        page7 = [self.label_Coil_wall_thickness, self.label_Overall_heat_transfer_coeficient, self.label_Log_mean_temperature_difference, self.label_Effective_mean_temperature_difference, self.label_Spiral_total_surface_area, self.label_Numbers_turns_coil, self.label_Height_of_cylinder]
        page8 = [self.label_coil_Factor_E, self.label_coil_Friction_factor, self.label_coil_Pressure_drop, self.label_shell_Drag_coeficient, self.label_shell_Pressure_drop, self.label_coil_Pumping_power, self.label_shell_Pumping_power]
        pages_to_reset = [page3, page4, page5, page6, page7, page8]

        i = 0
        for page in pages_to_reset:
            for item in page:
                if isinstance(item, QDoubleSpinBox):
                    if item != self.doubleSpinBox_hot_Inlet_temperature:
                        item.setValue(0)
                    else:
                        item.setValue(25)
                if isinstance(item, QLineEdit):
                    item.setText("")
                if i < 3:
                    item.setStyleSheet(self.error_handler.standard_style)
            i += 1

        selected = self.buttonGroup.checkedButton()
        if selected:
            self.buttonGroup.setExclusive(False)
            selected.setChecked(False)
            self.buttonGroup.setExclusive(True)

        self.stackedWidget.setCurrentIndex(0)

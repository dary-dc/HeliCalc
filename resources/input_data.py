class InputData:
    """
    This class is intended to create objects for storing 
    all the user inputs in the software


    * hot_parameter refers to the hot fluid parameter. Similarly, for cold_parameter.
    """
    def __init__(self):

        # 3rd page
        self.hot_fluid_name = ""
        self.cold_fluid_name = ""
    
        self.hot_in_shell = False
        self.hot_in_coil = False

        # 4th page
        self.cold_Mass_flowrate = 0
        self.cold_Inlet_temperature = 0
        self.cold_Outlet_temperature = 0
        self.cold_Fouling_factor = 0
        self.cold_Allowable_pressure_drop = 0

        self.cold_Density = 0
        self.cold_Viscosity = 0
        self.cold_Specific_heat = 0
        self.cold_Thermal_conductivity = 0

        self.hot_Mass_flowrate = 0
        self.hot_Inlet_temperature = 0
        self.hot_Outlet_temperature = 0
        self.hot_Fouling_factor = 0
        self.hot_Allowable_pressure_drop = 0

        self.hot_Density = 0
        self.hot_Viscosity = 0
        self.hot_Specific_heat = 0
        self.hot_Thermal_conductivity = 0

        # 5th page
        self.Shell_inner_diameter = 0
        self.Core_tube_outer_diameter = 0
        self.Average_spiral_diameter = 0
        self.Tube_outer_diameter = 0
        self.Tube_inner_diameter = 0
        self.Tube_pitch = 0
        self.Thermal_conductivity_coil_material = 0

        # for pages from 6 calculations
        self.coil_Mass_flowrate = 0
        self.coil_Density = 0
        self.coil_Viscosity = 0
        self.coil_Specific_heat = 0
        self.coil_Thermal_conductivity = 0
        self.coil_Fouling_factor = 0
        self.coil_Allowable_pressure_drop = 0

        self.shell_Mass_flowrate = 0
        self.shell_Density = 0
        self.shell_Viscosity = 0
        self.shell_Specific_heat = 0
        self.shell_Thermal_conductivity = 0
        self.shell_Fouling_factor = 0
        self.shell_Allowable_pressure_drop = 0

        # 7th
        self.Temperature_correction_factor = 0.99

        # 8th
        self.coil_Isentropic_efficiency_pump = 0.8
        self.shell_Isentropic_efficiency_pump = 0.8

    def initialize_attributes_with_hot_fluid_location(self):
        # for the calculations we need to convert the data
        # from the hot and cold fluids into the shell and 
        # coil-side fluids
        if self.hot_in_shell:
            self.coil_Mass_flowrate = self.cold_Mass_flowrate
            self.coil_Density = self.cold_Density
            self.coil_Viscosity = self.cold_Viscosity
            self.coil_Specific_heat = self.cold_Specific_heat
            self.coil_Thermal_conductivity = self.cold_Thermal_conductivity
            self.coil_Fouling_factor = self.cold_Fouling_factor
            self.coil_Allowable_pressure_drop = self.cold_Allowable_pressure_drop

            self.shell_Mass_flowrate = self.hot_Mass_flowrate
            self.shell_Density = self.hot_Density
            self.shell_Viscosity = self.hot_Viscosity
            self.shell_Specific_heat = self.hot_Specific_heat
            self.shell_Thermal_conductivity = self.hot_Thermal_conductivity
            self.shell_Fouling_factor = self.hot_Fouling_factor
            self.shell_Allowable_pressure_drop = self.hot_Allowable_pressure_drop

        elif self.hot_in_coil:
            self.shell_Mass_flowrate = self.cold_Mass_flowrate
            self.shell_Density = self.cold_Density
            self.shell_Viscosity = self.cold_Viscosity
            self.shell_Specific_heat = self.cold_Specific_heat
            self.shell_Thermal_conductivity = self.cold_Thermal_conductivity
            self.shell_Fouling_factor = self.cold_Fouling_factor
            self.shell_Allowable_pressure_drop = self.cold_Allowable_pressure_drop

            self.coil_Mass_flowrate = self.hot_Mass_flowrate
            self.coil_Density = self.hot_Density
            self.coil_Viscosity = self.hot_Viscosity
            self.coil_Specific_heat = self.hot_Specific_heat
            self.coil_Thermal_conductivity = self.hot_Thermal_conductivity
            self.coil_Fouling_factor = self.hot_Fouling_factor
            self.coil_Allowable_pressure_drop = self.hot_Allowable_pressure_drop
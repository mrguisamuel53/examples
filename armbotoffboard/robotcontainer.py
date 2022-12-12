# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

import wpilib
import constants
import commands2.button

from subsystems.armsubsystem import ArmSubsystem
from subsystems.drivesubsystem import DriveSubsystem

class RobotContainer:
    
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:
        # The robot's subsystems
        self.robotDrive = DriveSubsystem()
        self.robotArm = ArmSubsystem()
        
        # The driver's controller
        self.driverController = wpilib.XboxController(constants.kDriverControllerPort)
        #self.driverController = wpilib.Joystick(constants.kDriverControllerPort)

        # Configure the button bindings
        self.configureButtonBindings()

        # Set the default drive command
        self.robotDrive.setDefaultCommand(
            commands2.RunCommand(
                lambda: self.robotDrive.arcadeDrive(
                    lambda: -self.driverController.getLeftY(),
                    lambda: self.driverController.getRightX()
                ),
                [self.robotDrive]
            )
        )

    def configureButtonBindings(self) -> None:
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """

        # Move the arm to 2 radians above horizontal when the 'A' button is pressed.
        commands2.button.JoystickButton(
            self.driverController, wpilib.XboxController.Button.kA 
        ).whenPressed(commands2.InstantCommand(lambda: self.robotArm.setGoal(2), self.robotArm))

        # Move the arm to neutral position when the 'B' button is pressed.
        commands2.button.JoystickButton(
            self.driverController, wpilib.XboxController.Button.kB
        ).whenPressed(commands2.InstantCommand(lambda: self.robotArm.setGoal(constants.kArmOffsetRads), self.robotArm))

        # Drive at half speed when some of bumpers are held.
        commands2.button.JoystickButton(
            self.driverController, wpilib.XboxController.Button.kRightBumper
        ).whenPressed(commands2.InstantCommand(lambda: self.robotDrive.setMaxOutput(0.5)))
        
        commands2.button.JoystickButton(
            self.driverController, wpilib.XboxController.Button.kLeftBumper
        ).whenReleased(commands2.InstantCommand(lambda: self.robotDrive.setMaxOutput(1)))
    
    def getAutonomousCommand(self) -> commands2.Command:
        return commands2.InstantCommand()
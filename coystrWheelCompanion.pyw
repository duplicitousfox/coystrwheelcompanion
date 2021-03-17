# coystrWheel Companion v1.0.6
# Created by DuplicitousFox for Coy_Stream@twitch.tv
# (c)2020, 2021 Foxtail Studios

# v.1.0: Initial Release
# v.1.0.1: Added a function that shows the text file's users and weights
#         	Bugfix: Corrected an issue where Weight would not update on use of "All Weight+1" in the main window
# v.1.0.2: Added a confirmation box to the Remove button.
# 			Bugfix: Corrected an issue where using Remove would display the wrong name.
# v.1.0.3: Bugfix: Corrected an issue where trying to use Remove on the last remaining item in the list would crash the program.
#					Corrected an issue found when using Remove on the last remaining item (after the above fix) would not clear input fields.
# v.1.0.4: Added separate buttons for randomizing Background and Text color values individually.
#			Changed the default BG and Text colors to black and white in the "Add New..." menu, respectively.
#			Enabled "." and "'" as valid entries in the "Add New..." menu's Name input box.
# v.1.0.5: Changed where popup windows spawn. It is now based on where the main window is currently located.
#			Bugfix: Corrected an issue where it was possible to add a piece to the wheel without a name, which crashed the program.
# v.1.0.6: Added a feature that checks if someone's already on the list when using "Add to Wheel", prevents the addition, and
#			brings the user to that person's name in the list.

import PySimpleGUI as sg
import random

# Variable declarations from file

file = open('wheeldata.txt', 'a+')
file.close()
file = open('wheeldata.txt')
content = file.readlines()
selectLength = len(content) # sets the upper limit based on how many items are in the list.
choices = []
file.close()
win_icon = 'ftsico.ico'
separator = " "
random.seed()

#print(content) #for debug purposes only

# Parse and generate a list of names this program can use from wheeldata.txt

for i in range(selectLength):
	nameList = content[i].split()
	choices.append(nameList[7])

# GUI Declarations

def main_win():
	menu_def = [['Help', ['Help...', 'About...']], ]
	title = "coystrWheel Companion"
	layout = [[sg.Menu(menu_def)],
			[sg.Text('Select Piece:          '), sg.Text('BG Color (#RRGGBB)'), sg.Text('Text Color (#RRGGBB)'), sg.Text('Weight')],
			[sg.Combo(choices, size=(15, 5), key='-selection-', enable_events=True), sg.Text('#'), sg.Input(size=(3, 1), key='-R1-', enable_events=True), sg.Input(size=(3, 1), key='-G1-', enable_events=True), sg.Input(size=(3, 1), key='-B1-', enable_events=True), sg.Text('      #'), sg.Input(size=(3, 1), key='-R2-', enable_events=True), sg.Input(size=(3, 1), key='-G2-', enable_events=True), sg.Input(size=(3, 1), key='-B2-', enable_events=True), sg.Text('  '), sg.Input(size=(3, 1), key='-WEIGHT-', enable_events=True), sg.Button('Apply')],
			[sg.Button('Add New...'), sg.Button('Remove'), sg.Button('All Weight+1'), sg.Button('Show List'), sg.Button('Save')]]
	return sg.Window(title, layout, icon = win_icon, finalize=True)

def addnew_win():
	title = "Add New..."
	layout = [[sg.Text('Name:'), sg.Input(key='-NAMEIN-', background_color='#000000', text_color='#ffffff', enable_events=True)],
		[sg.Text('BG Color: #'), sg.Input(default_text="00", size=(3, 1), key='-R1IN-', enable_events=True), sg.Input(default_text="00", size=(3, 1), key='-G1IN-', enable_events=True), sg.Input(default_text="00", size=(3, 1), key='-B1IN-', enable_events=True), sg.Button('Randomize BG Color')],
		[sg.Text('Name Color: #'), sg.Input(default_text="ff", size=(3, 1), key='-R2IN-', enable_events=True), sg.Input(default_text="ff", size=(3, 1), key='-G2IN-', enable_events=True),sg.Input(default_text="ff", size=(3, 1), key='-B2IN-', enable_events=True), sg.Button('Randomize Text Color')],
		[sg.Checkbox('Subscriber', key='-SUBIN-'), sg.Button('Randomize Both Colors')],
		[sg.Button('Add to Wheel'), sg.Button('Cancel')]]

	return sg.Window(title, layout, icon = win_icon, finalize=True)

def main():
	window1, window2 = main_win(), None
	var8 = ' '
	selectIndex = 0

	while True:  #event Loop
		window, event, values = sg.read_all_windows()

		locale_tuple = (window1.CurrentLocation()) # Set up where the windows will spawn by finding window1's location
		locale = list(locale_tuple) # Tuples are immutable. Gotta store it as a list.
		locale[0] = locale[0] + (window1.Size[0] / 4) # Edit x window coordinate
		locale[1] = locale[1] + (window1.Size[1] / 2) # Edit y window coordinate
		sg.SetOptions(window_location = locale) # All future windows will spawn here.
		
		if window == sg.WIN_CLOSED:  #if all windows were closed
			break
		if event == sg.WIN_CLOSED or event == 'Cancel' or event == 'Close':
			window.close()
			if window == window2:
				window2 = None
			elif window == window1:
				break
		elif event == 'Help...':
			sg.popup('How to use coystrWheel Companion', 'Select a name from the dropdown to load and edit an existing piece. When finished editing a single piece, press the Apply button.', 'The Add New... button will pop up a new window for you to enter data and add it to the wheel. Maximum name length is 15 characters. RGB values are in Hexidecimal.', 'The Remove button will remove the currently selected piece from the wheel.', 'The All Weight+1 button adds 1 to all of the pieces weights.', 'When you are finished, click Save. Your changes will ONLY commit to file when you click Save, so do not forget to do this!', location = locale)
		elif event == 'About...':
			sg.popup('coystrWheel Version 1.0.3', 'coystrWheel Companion Version 1.0.6', "For my good friend, Coy. Hope all your seeds aren't trash!", location = locale)
			sg.popup('Seriously, though...', 'If something breaks, hit me up on Discord.', '--Hidari', location = locale)
		elif event == 'Add New...':
			if not window2:
				window2 = addnew_win()
		elif event == 'Apply' and values['-selection-']: # edit the current piece
			content[selectIndex] = str(int(values['-WEIGHT-'], 10)) + " " + str(int(values['-R1-'], 16)) + " " + str(int(values['-G1-'], 16)) + " " + str(int(values['-B1-'], 16)) + " " + str(int(values['-R2-'], 16)) + " " + str(int(values['-G2-'], 16)) + " " + str(int(values['-B2-'], 16)) + " " + var8 + "\n"
			sg.popup('Changes applied successfully.', location = locale)
			#print(content) # debug purposes only
		elif event == 'Remove' and values['-selection-']: # remove the current piece, gotta confirm first
			deletedName = choices[selectIndex]
			elephant = sg.popup_yes_no('Removing ' + deletedName + ' from the wheel. Are you sure?', title='Warning: Confirmation Required!', location = locale)
			if elephant == 'Yes':
				content.pop(selectIndex)
				choices.pop(selectIndex)
				if content != []: #if there's more on the wheel...
					values['-selection-'] = values['-selection-'][0]
					selectIndex = 0
					window.FindElement('-selection-').update(set_to_index = selectIndex, values=choices)
					selectList = content[selectIndex].split()
					var1, var2, var3, var4, var5, var6, var7 = [hex(int(selectList[k])).lstrip("0x").zfill(2) for k in range(7)]
					var1 = int(var1, 16)
					var8 = selectList[7]
					window['-WEIGHT-'].update(var1)
					window['-R1-'].update(var2), window['-G1-'].update(var3), window['-B1-'].update(var4)
					window['-R2-'].update(var5), window['-G2-'].update(var6), window['-B2-'].update(var7)
				else: #nothing else is left
					values['-selection-'] = ['']
					selectIndex = 0
					window['-selection-'].update('', set_to_index = -1, values=choices)
					window['-WEIGHT-'].update('')
					window['-R1-'].update(''), window['-G1-'].update(''), window['-B1-'].update('')
					window['-R2-'].update(''), window['-G2-'].update(''), window['-B2-'].update('')
				sg.popup(deletedName + ' removed from the wheel successfully.', location = locale)
			else:
				continue
			#print(content) # debug purposes only
		elif event == 'All Weight+1' and len(choices) > 0: # add +1 to all pieces weight
			for i in range(len(content)):
				weightList = content[i].split()
				weightMod = int(weightList[0], 10) + 1
				weightList[0] = str(weightMod)
				content[i] = separator.join(weightList) + "\n"
			if values['-selection-']:
				selectList = content[selectIndex].split()
				var1 = int(selectList[0])
				window['-WEIGHT-'].update(var1)
			sg.popup('All weights increased by +1 successfully.', location = locale)
			#print(content) # debug purposes only
		elif event == 'Show List': # Generate a list of everything on the wheel
			sg.PrintClose()
			sg.Print('Number  Weight  Name')
			for i, j in enumerate(content):
				showList = content[i].split()
				showWeight = showList[0]
				showName = showList[7]
				sg.Print(' ' + str(int(i+1)).zfill(3) + '      ' + str(showWeight).zfill(2) + '    ' + showName)
		elif event == 'Save': # write to file
			file = open('wheeldata.txt','w')
			file.writelines(content)
			file.close()
			sg.popup('Your data has been saved.', location = locale)
		elif event == '-NAMEIN-' and values['-NAMEIN-'] and values['-NAMEIN-'][-1] not in ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-'."):
			window['-NAMEIN-'].update(values['-NAMEIN-'][:-1])
		elif event == '-NAMEIN-' and len(values['-NAMEIN-']) > 15:
			window['-NAMEIN-'].update(values['-NAMEIN-'][:-1])
		elif event == '-WEIGHT-' and values['-WEIGHT-'] and values['-WEIGHT-'][-1] not in ('0123456789'):
			window['-WEIGHT-'].update(values['-WEIGHT-'][:-1])
		elif event == '-R1-' and values['-R1-'] and values['-R1-'][-1] not in ('0123456789abcdefABCDEF'):
			window['-R1-'].update(values['-R1-'][:-1])
		elif event == '-R1-' and len(values['-R1-']) > 2:
			window['-R1-'].update(values['-R1-'][:-1])
		elif event == '-G1-' and values['-G1-'] and values['-G1-'][-1] not in ('0123456789abcdefABCDEF'):
			window['-G1-'].update(values['-G1-'][:-1])
		elif event == '-G1-' and len(values['-G1-']) > 2:
			window['-G1-'].update(values['-G1-'][:-1])
		elif event == '-B1-' and values['-B1-'] and values['-B1-'][-1] not in ('0123456789abcdefABCDEF'):
			window['-B1-'].update(values['-B1-'][:-1])
		elif event == '-B1-' and len(values['-B1-']) > 2:
			window['-B1-'].update(values['-B1-'][:-1])
		elif event == '-R1IN-' and values['-R1IN-'] and values['-R1IN-'][-1] not in ('0123456789abcdefABCDEF'):
			window['-R1IN-'].update(values['-R1IN-'][:-1])
		elif event == '-R1IN-' and len(values['-R1IN-']) > 2:
			window['-R1IN-'].update(values['-R1IN-'][:-1])
		elif event == '-G1IN-' and values['-G1IN-'] and values['-G1IN-'][-1] not in ('0123456789abcdefABCDEF'):
			window['-G1IN-'].update(values['-G1IN-'][:-1])
		elif event == '-G1IN-' and len(values['-G1IN-']) > 2:
			window['-G1IN-'].update(values['-G1IN-'][:-1])
		elif event == '-B1IN-' and values['-B1IN-'] and values['-B1IN-'][-1] not in ('0123456789abcdefABCDEF'):
			window['-B1IN-'].update(values['-B1IN-'][:-1])
		elif event == '-B1IN-' and len(values['-B1IN-']) > 2:
			window['-B1IN-'].update(values['-B1IN-'][:-1])
		elif event == '-R2-' and values['-R2-'] and values['-R2-'][-1] not in ('0123456789abcdefABCDEF'):
			window['-R2-'].update(values['-R2-'][:-1])
		elif event == '-R2-' and len(values['-R2-']) > 2:
			window['-R2-'].update(values['-R2-'][:-1])
		elif event == '-G2-' and values['-G2-'] and values['-G2-'][-1] not in ('0123456789abcdefABCDEF'):
			window['-G2-'].update(values['-G2-'][:-1])
		elif event == '-G2-' and len(values['-G2-']) > 2:
			window['-G2-'].update(values['-G2-'][:-1])
		elif event == '-B2-' and values['-B2-'] and values['-B2-'][-1] not in ('0123456789abcdefABCDEF'):
			window['-B2-'].update(values['-B2-'][:-1])
		elif event == '-B2-' and len(values['-B2-']) > 2:
			window['-B2-'].update(values['-B2-'][:-1])
		elif event == '-R2IN-' and values['-R2IN-'] and values['-R2IN-'][-1] not in ('0123456789abcdefABCDEF'):
			window['-R2IN-'].update(values['-R2IN-'][:-1])
		elif event == '-R2IN-' and len(values['-R2IN-']) > 2:
			window['-R2IN-'].update(values['-R2IN-'][:-1])
		elif event == '-G2IN-' and values['-G2IN-'] and values['-G2IN-'][-1] not in ('0123456789abcdefABCDEF'):
			window['-G2IN-'].update(values['-G2IN-'][:-1])
		elif event == '-G2IN-' and len(values['-G2IN-']) > 2:
			window['-G2IN-'].update(values['-G2IN-'][:-1])
		elif event == '-B2IN-' and values['-B2IN-'] and values['-B2IN-'][-1] not in ('0123456789abcdefABCDEF'):
			window['-B2IN-'].update(values['-B2IN-'][:-1])
		elif event == '-B2IN-' and len(values['-B2IN-']) > 2:
			window['-B2IN-'].update(values['-B2IN-'][:-1])
		elif event == '-R1IN-' or event == '-G1IN-' or event == '-B1IN-' or event == '-R2IN-' or event == '-G2IN-' or event == '-B2IN-':
			valRRGGBB1 = "#" + (values['-R1IN-']).zfill(2) + (values['-G1IN-']).zfill(2) + (values['-B1IN-']).zfill(2)
			valRRGGBB2 = "#" + (values['-R2IN-']).zfill(2) + (values['-G2IN-']).zfill(2) + (values['-B2IN-']).zfill(2)
			window['-NAMEIN-'].update(text_color = valRRGGBB2, background_color = valRRGGBB1)
		elif event == 'Randomize BG Color':
			rngR1 = hex(int(random.randrange(0, 255, 1))).lstrip("0x").zfill(2)
			rngG1 = hex(int(random.randrange(0, 255, 1))).lstrip("0x").zfill(2)
			rngB1 = hex(int(random.randrange(0, 255, 1))).lstrip("0x").zfill(2)
			window['-R1IN-'].update(rngR1), window['-G1IN-'].update(rngG1), window['-B1IN-'].update(rngB1)
			valRRGGBB1 = "#"+str(rngR1)+str(rngG1)+str(rngB1)
			window['-NAMEIN-'].update(background_color = valRRGGBB1)
		elif event == 'Randomize Text Color':
			rngR2 = hex(int(random.randrange(0, 255, 1))).lstrip("0x").zfill(2)
			rngG2 = hex(int(random.randrange(0, 255, 1))).lstrip("0x").zfill(2)
			rngB2 = hex(int(random.randrange(0, 255, 1))).lstrip("0x").zfill(2)
			window['-R2IN-'].update(rngR2), window['-G2IN-'].update(rngG2), window['-B2IN-'].update(rngB2)
			valRRGGBB2 = "#"+str(rngR2)+str(rngG2)+str(rngB2)
			window['-NAMEIN-'].update(text_color = valRRGGBB2)
		elif event == 'Randomize Both Colors':
			rngR1 = hex(int(random.randrange(0, 255, 1))).lstrip("0x").zfill(2)
			rngG1 = hex(int(random.randrange(0, 255, 1))).lstrip("0x").zfill(2)
			rngB1 = hex(int(random.randrange(0, 255, 1))).lstrip("0x").zfill(2)
			rngR2 = hex(int(random.randrange(0, 255, 1))).lstrip("0x").zfill(2)
			rngG2 = hex(int(random.randrange(0, 255, 1))).lstrip("0x").zfill(2)
			rngB2 = hex(int(random.randrange(0, 255, 1))).lstrip("0x").zfill(2)
			window['-R1IN-'].update(rngR1), window['-G1IN-'].update(rngG1), window['-B1IN-'].update(rngB1)
			window['-R2IN-'].update(rngR2), window['-G2IN-'].update(rngG2), window['-B2IN-'].update(rngB2)
			valRRGGBB1 = "#"+str(rngR1)+str(rngG1)+str(rngB1)
			valRRGGBB2 = "#"+str(rngR2)+str(rngG2)+str(rngB2)
			window['-NAMEIN-'].update(text_color = valRRGGBB2, background_color = valRRGGBB1)
		elif event == 'Add to Wheel' and values['-NAMEIN-']: # put all the stuff into the list as a new wheel piece
			if values['-NAMEIN-'] in choices: # if someone's already on the list, notify the user
				sg.popup('Error: ' + values['-NAMEIN-'] + ' is already on the wheel.')
				i = 0
				while i < len(choices):
					if values['-NAMEIN-'] == choices[i]:
						selectIndex = i
					i += 1
				if window == window2: # close the window and set the list to the name specified
					window.close()
					window2 = None
				output_window = window1
				if output_window:
					output_window['-selection-'].update(set_to_index = selectIndex, values=choices)
					selectList = content[selectIndex].split()
					var1, var2, var3, var4, var5, var6, var7 = [hex(int(selectList[k])).lstrip("0x").zfill(2) for k in range(7)]
					var1 = int(var1, 16)
					var8 = selectList[7]
					output_window['-WEIGHT-'].update(var1)
					output_window['-R1-'].update(var2), output_window['-G1-'].update(var3), output_window['-B1-'].update(var4)
					output_window['-R2-'].update(var5), output_window['-G2-'].update(var6), output_window['-B2-'].update(var7)
					output_window = None
				continue
			if values['-SUBIN-']:
				subweight = 5
			else:
				subweight = 1
			if len(content) > 0:
				prevline = content[len(content)-1]
				lastchar = prevline[-1]
				if lastchar != "\n":
					content[len(content)-1] = content[len(content)-1] + "\n"
			addnew_user = (str(subweight) + ' ' + str(int(values['-R1IN-'], 16)) + ' ' + str(int(values['-G1IN-'], 16)) + ' ' + str(int(values['-B1IN-'], 16)) + ' ' + str(int(values['-R2IN-'], 16)) + ' ' + str(int(values['-G2IN-'], 16)) + ' ' + str(int(values['-B2IN-'], 16)) + ' ' + values['-NAMEIN-'])
			content.append(addnew_user)
			choices.append(values['-NAMEIN-'])
			#print(content) # for debug purposes only
			sg.popup(values['-NAMEIN-'] + ' added to the wheel successfully.', location = locale)
			if window == window2:
				window.close()
				window2 = None
			output_window = window1
			if output_window:
				selectIndex = len(choices) - 1
				output_window['-selection-'].update(set_to_index = selectIndex, values=choices)
				selectList = content[selectIndex].split()
				var1, var2, var3, var4, var5, var6, var7 = [hex(int(selectList[k])).lstrip("0x").zfill(2) for k in range(7)]
				var1 = int(var1, 16)
				var8 = selectList[7]
				output_window['-WEIGHT-'].update(var1)
				output_window['-R1-'].update(var2), output_window['-G1-'].update(var3), output_window['-B1-'].update(var4)
				output_window['-R2-'].update(var5), output_window['-G2-'].update(var6), output_window['-B2-'].update(var7)
				output_window = None

		try:
			if values['-selection-'] and values['-selection-'] != var8 and values['-selection-'] != ['']:
				for i, j in enumerate(choices):
					if j == values['-selection-']:
						selectIndex = i
						selectList = content[selectIndex].split()
						var1, var2, var3, var4, var5, var6, var7 = [hex(int(selectList[k])).lstrip("0x").zfill(2) for k in range(7)]
						var1 = int(var1, 16)
						var8 = selectList[7]
				window['-WEIGHT-'].update(var1)
				window['-R1-'].update(var2), window['-G1-'].update(var3), window['-B1-'].update(var4)
				window['-R2-'].update(var5), window['-G2-'].update(var6), window['-B2-'].update(var7)
		except KeyError:
			continue

if __name__ == "__main__":
	main()
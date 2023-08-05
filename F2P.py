#pip install numpy pandas matplotlib


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Reading the Data from path
directory_location = input("Please import the directory your data located: ")
Saving_location = input("Please import the directory you want your analyzed data saved: ")
filename = input("By which name you want your analyzed data to be saved: ")

# Reading the Online analysis.txt file
loc_1 = directory_location + '/online analysis.txt'
online_analysis = pd.read_table(loc_1, sep='\t').to_numpy()

# Reading the data_user input.csv
loc_2 = directory_location + '/data_user input.csv'
user_input = pd.read_csv(loc_2).to_numpy()

# Reading the Results.csv
loc = directory_location + '/Results.csv'
Data_table = pd.read_csv(loc)
Data = Data_table.to_numpy()

# Acquiring time frame and E-phys
Time_frame = online_analysis[1, 1] - online_analysis[0, 1]
E_phys = user_input[:len(Data[:, 0]), 1]
Data = np.column_stack((E_phys, Data))

# Detecting where the E-Phys is above the threshold and eliminate the
# values at that points from the Data
threshold = 1
idx = np.where(Data[:, 0] > threshold)[0]
Data = np.delete(Data, idx, axis=0)

# Taking two sec before and after excitation and Calculating df/f
two_sec = int(2000 / Time_frame)  # Each sec is 1000 msec
F_0 = np.zeros(Data.shape[1] - 1)
for i in range(1, Data.shape[1]):
    F_0[i - 1] = np.mean(Data[idx[0] - two_sec:idx[0], i])

# Calculating dF/F = (F(t)/F0) - 1
for i in range(1, Data.shape[1]):
    Data[:, i] = (Data[:, i] / F_0[i - 1]) - 1

# Concatenated version of Data for 2 sec before and after
Data_conc = Data[idx[0] - two_sec:idx[0] + two_sec, 1:]

# Separate Data for 2 sec before and 2 sec after
Data_before = Data[idx[0] - two_sec:idx[0], 1:]
Data_after = Data[idx[0]:idx[0] + two_sec, 1:]

# Make a matrix that is the combination of Data_before and Data_after
row_Data_final = Data_after.shape[0]
column_Data_final = 2 * Data_after.shape[1]  # Number of rows must be twice of each separated Data
Data_final = np.zeros((row_Data_final, column_Data_final))
for i in range(Data_after.shape[1]):
    Data_final[:, 2 * i] = Data_before[:, i]
    Data_final[:, 2 * i + 1] = Data_after[:, i]

# Arranging the output file in an Excel sheet
Header = Data_table.columns
Header = [header.replace("Mean_", "").replace("_", " (") + ")" for header in Header]
Header_Data = [header for sublist in zip(Header, Header) for header in sublist]
Results = pd.DataFrame(Data_final, columns=Header_Data)
Results.to_excel(f"{Saving_location}/{filename}.xlsx", index=False)

# Plotting Concatenated Data
plt.figure(1)
plt.plot(Data_conc, linewidth=3)
plt.legend(Header)
plt.xlabel("Time point")
plt.ylabel(r"$\Delta$f/f = (f_t - f_0) - 1")
plt.title(r"$\Delta$f/f for 2 seconds before and after the first stimulus")

# Plotting Concatenated Data
plt.figure(2)
plt.plot(Data_before, linewidth=3)
plt.plot(Data_after, linewidth=3)
plt.legend(Header_Data)
plt.xlabel("Time point")
plt.ylabel(r"$\Delta$f/f = (f_t - f_0) - 1")
plt.title(r"$\Delta$f/f for 2 seconds before and after the first stimulus (separated)")

plt.show()

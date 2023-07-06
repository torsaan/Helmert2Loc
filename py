import numpy as np
import matplotlib.pyplot as plt

#f15->16 , p2 for graph

def helmert_transform(point, origin, dx, dy, theta):
    rotation_matrix = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)]
    ])
    transformed_point = np.matmul(rotation_matrix, point - origin) + origin + np.array([dx, dy])
    return transformed_point


#  origin 
M25_89 = np.array([6740424.500, 591432.000])
M10_89 = np.array([6740442.258, 591453.542])
M25_LOC = np.array([100, 200])
M10_LOC = np.array([100, 210])

# translation and rotation
dx, dy = M25_LOC - M25_89
theta = np.arctan2(M10_LOC[1] - M25_LOC[1], M10_LOC[0] - M25_LOC[0]) - np.arctan2(M10_89[1] - M25_89[1], M10_89[0] - M25_89[0])

# transformation
points_euref89 = np.array([
    [6740484.723 , 591450.315],#A         185.237
[6740470.129 , 591462.909],#B         185.374
[6740460.482 , 591471.329],#C         184.246
[6740438.106 , 591465.353],#D         185.074
[6740415.732 , 591472.566],#E         185.347
[6740400.375 , 591454.093],#F         185.261
[6740460.354 , 591518.477],#P1        183.075
#[6740253.871 , 590936.840],#P2        191.011
[6740381.018 , 591414.029],#S1        185.473
[6740432.895 , 591387.513],#S2        183.471
[6740518.278 , 591466.545],#S3        184.145
[6740424.500 , 591432.000],#M25       184.000
[6740441.667 , 591417.849],#A25       184.000
[6740442.258 , 591453.542],#M10       184.000
[6740446.550 , 591450.005],#J10       184.000
[6740459.425 , 591439.391],#A10       184.000
[6740457.014 , 591462.699],#J1        184.000
[6740469.890 , 591452.086],#A1        184.000
[6740459.247 , 591453.749],#F4        184.000
[6740441.608 , 591456.412],#FRI1        0.000
[6740424.522 , 591431.986],#StkdM25    -0.158
[6740442.238 , 591453.538],#StkdM10    -0.185
[6740446.564 , 591450.022],#StkdJ10    -0.210
[6740441.665 , 591417.855],#StkdA25    -0.292
[6740457.014 , 591462.706],#StkdJ1     -0.019
[6740459.298 , 591453.749],#StkdF4     -0.151
[6740469.875 , 591452.094],#StkdA1     -0.048
[6740459.430 , 591439.390],#StkdA10    -0.252
[6740441.628 , 591435.977],#ANGSM25M1  -0.257
[6740442.173 , 591453.552] #StkdM10H    1.000
    
])
euref89_origin = M25_89
points_local = [helmert_transform(point, euref89_origin, dx, dy, theta) for point in points_euref89]

# Print transformation parameters
print("Translation (dx, dy):", (dx, dy))
print("Rotation (theta):", np.degrees(theta), "degrees")

#Extra Poiint
def transform_new_points(points):
    return [helmert_transform(point, euref89_origin, dx, dy, theta) for point in points]

# Extra
new_points_euref89 = np.array([
    # Extra
])

new_points_local = transform_new_points(new_points_euref89)










# inverse transformation for the black line
def inverse_helmert_transform(point, origin, dx, dy, theta):
    rotation_matrix = np.array([
        [np.cos(-theta), -np.sin(-theta)],
        [np.sin(-theta), np.cos(-theta)]
    ])
    transformed_point = np.matmul(rotation_matrix, point - origin - np.array([dx, dy])) + origin
    return transformed_point

euref89_x_line_endpoints = [inverse_helmert_transform(np.array([100, y]), euref89_origin, dx, dy, theta) for y in [0, 400]]
euref89_y_line_endpoints = [inverse_helmert_transform(np.array([x, 200]), euref89_origin, dx, dy, theta) for x in [0, 400]]

def plot_points(points_euref89, points_local, point_names):
    # EUREF89 plot
    fig1, ax1 = plt.subplots(figsize=(10, 10))
    ax1.scatter(points_euref89[:, 0], points_euref89[:, 1], color='blue', label='EUREF89')
    for i, name in enumerate(point_names):
        ax1.text(points_euref89[i, 0], points_euref89[i, 1], name)
    ax1.set_title('Points in EUREF89')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.grid(True)
    ax1.legend()

    # Draw black lines in EUREF89 plot
    ax1.plot([euref89_x_line_endpoints[0][0], euref89_x_line_endpoints[1][0]], [euref89_x_line_endpoints[0][1], euref89_x_line_endpoints[1][1]], color='black')
    ax1.plot([euref89_y_line_endpoints[0][0], euref89_y_line_endpoints[1][0]], [euref89_y_line_endpoints[0][1], euref89_y_line_endpoints[1][1]], color='black')
#X y Limits for Euref
    ax1.set_xlim(6740410.667, 6740490)
    ax1.set_ylim(591350.000, 591550.000)
    # Local plot
    fig2, ax2 = plt.subplots(figsize=(10, 10))
    ax2.scatter(points_local[:, 0], points_local[:, 1], color='red', label='Local')
    for i, name in enumerate(point_names):
        ax2.text(points_local[i, 0], points_local[i, 1], name)
    ax2.set_title('Points in Local Coordinate System')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.grid(True)
    ax2.legend()

    # Draw black lines in Local Coordinate System plot
    ax2.plot([100, 100], [0, 400], color='black')
    ax2.plot([0, 400], [200, 200], color='black')
    # Set the x and y limits for the Local Coordinate System plot
    ax2.set_xlim(50, 175)
    ax2.set_ylim(90, 325)

    plt.show()





# Convert the list to array
points_local = np.array(points_local)

# Define point names
point_names = ['A','B','C','D','E','F','P1'#,'P2'
               ,'S1','S2','S3','M25','A25','M10','J10','A10','J1','A1','F4','FRI1','StkdM25','StkdM10','StkdJ10','StkdA25','StkdJ1','StkdF4','StkdA1','StkdA10','ANGSM25M1','StkdM10H']

# Function to print transformed coordinates 
def print_transformed_coordinates(points_local, point_names):
    print("\nTransformed Coordinates (Local):")
    print("{:<5} {:>12} {:>12}".format("Name", "X", "Y"))
    print("-" * 29)
    for i, point in enumerate(points_local):
        print("{:<5} {:>12.3f} {:>12.3f}".format(point_names[i], point[0], point[1]))

# Call the function to print the transformed coordinates
print_transformed_coordinates(points_local, point_names)

# Plot the points with tag
plot_points(points_euref89, points_local, point_names)
new_points_local = transform_new_points(new_points_euref89)

# Print transformation parameters
print("Translation (dx, dy):", (dx, dy))
print("Rotation (theta):", np.degrees(theta), "degrees")

# Define point names
point_names = [
    'A', 'B', 'C', 'D', 'E', 'F', 'P1', #'P2'
    'S1', 'S2', 'S3', 'M25', 'A25', 'M10', 'J10', 'A10', 'J1', 'A1', 'F4', 'FRI1', 'StkdM25', 'StkdM10', 'StkdJ10', 'StkdA25', 'StkdJ1', 'StkdF4', 'StkdA1', 'StkdA10', 'ANGSM25M1', 'StkdM10H'
]

# Print  old and new 
print("\n{:<10} {:<15} {:<15} {:<15} {:<15}".format("Name", "EUREF89_X", "EUREF89_Y", "Local_X", "Local_Y"))
for name, old_point, new_point in zip(point_names, points_euref89, points_local):
    print("{:<10} {:<15.3f} {:<15.3f} {:<15.3f} {:<15.3f}".format(name, old_point[0], old_point[1], new_point[0], new_point[1]))

from bokeh.plotting import figure, output_file, show

def plotGraphs(trainf_list, testv_list):
    '''
    Plots graphs for given functions
            Parameters:
                    trainf_list (list of TrainingFunction): the given training function list 
                    testv_list (list of TestFunction): a list of all test values
    '''
    # iterate through trainf_list to plot one graph for all 4 training functions 
    for tf in trainf_list:
        # naming the html page 
        output_file("trainingfunction{}.html".format(tf.name))
        # defining plot with title, axes and dimensions
        plot = figure(title="training function {} and matching ideal function {} "
                    .format(tf.name, tf.matching_ideal_f.name ),
                    x_axis_label ="x",
                    y_axis_label = "y",
                    plot_width=1450, plot_height=850)

        # drawing line plot for training values
        plot.line(tf.x_values, 
            tf.y_values, 
            legend_label = "training function", 
            line_color="darkslateblue",
            line_width = 2)
        # drawing line plot for ideal values 
        plot.line(tf.matching_ideal_f.x_values, 
            tf.matching_ideal_f.y_values, 
            legend_label = "ideal function", 
            line_color="hotpink",
            line_width = 2)
        
        test_x = []
        test_y = []
        # looping through the testv_list, to find all test values, which match with the current ideal function
        for tv in testv_list:
            if(tv.matching_ideal_f_name == tf.matching_ideal_f.name):
                #adding the matching x and y values to lists
                test_x.append(tv.x_values)
                test_y.append(tv.y_values)

        # drawing dots for the matching test values
        plot.circle(test_x, test_y, size = 7, color = "orangered", legend_label = "matched test values")
        show(plot)
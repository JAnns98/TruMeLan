#Data is big endian format so have to use >... for datatype (eg >I) for unsigned integer

def MovrHeader(file):
    """
    Function for reading and outputting the header of a movr file

    Parameters
    ----------
    file : Str
        The .movr file input.

    Returns
    -------
    df1 : DataFrame
        A dataframe of the movrheader information.

    """
    import struct
    import pandas as pd
    input_file_name = (file)
    input_file = open(input_file_name, 'rb')                                   #Have to specify 'rb' for readbytes rather than writing a file
    data = input_file.read(1)
    data1 = input_file.read(16)
    filetype_version = struct.unpack("B", data)
    header = struct.unpack(">4i", data1)
    header_length= input_file.tell() #.tell() function shows you how many bytes have been read so far
    cols = ['Filetype_Version', 'Header_Version', 'Image_Xres', 'Image_Yres', 'Record_Size', 'Header_Length']
    lst = []
    lst.append([filetype_version[0], header[0], header[1], header[2],header[3], header_length])
    df1 = pd.DataFrame(lst, columns=cols)
    return df1

def MovrRecordSelector(file, s,f):
    """
    A function that selects and prints the records in the .movr file given your selection

    Parameters
    ----------
    file : Str
        The input .movr file.
    s : Int
        The start frame.
    f : Int
        The final frame.

    Returns
    -------
    df1 : DataFrame
        A dataframe with each row as a record for the records selected.

    """
    
    from matplotlib import pyplot as plt
    import numpy as np
    import struct
    from datetime import datetime
    import pandas as pd
    input_file_name = (file)
    input_file = open(input_file_name, 'rb')
    data = input_file.read(1)
    data1 = input_file.read(16)
    struct.unpack("B", data)
    header = struct.unpack(">4i", data1)
    input_file.tell() #.tell() function shows you how many bytes have been read so far
    
    cols = ['Record Number', 'Frame Number', 'Timestamp (ms)', 'DateTime', 'Error_code', 'Areapix', 'cXpix', 'cYpix',
           'Orientation','Top_pix','Bounding_Diag','Axis_X1','Axis_Y1','Axis_X2','Axis_Y2','cXmm','cX','cYmm','cY',
           'Top_mm','Vx_mm_per_sec','Vy_mm_per_sec','Orbital_deg','Orbital_radius','Orbital_deg_per_sec','Noise_level','Vx_Av_mm_per_sec','Vy_Av_mm_per_sec','W_Av_deg_per_sec',
           'Track_deg','Speed_mm_per_sec','Speed_Av_mm_per_sec','dXmm','dYmm','distance_mm','Heading_deg','HeadingConf','Length','HeadX_pix','HeadY_pix']
    lst = []

    input_file.seek(header[3]*s, 1)                                            #This function will skip through to the first record you are actually interested in
    for n in range(s,f):                                                       #For loop here allows to loop through one record at a time
        
        data2 = input_file.read(4)
        frame_num = struct.unpack(">I", data2)
        
        data3 = input_file.read(4)
        ms_time = struct.unpack(">I", data3)
        
        data4 = input_file.read(8)
        ab_time = struct.unpack(">q", data4)
        timestamp = ab_time[0]-2082816000
       
        data4b=input_file.read(8)
        fraction = struct.unpack(">Q", data4b)
        time = timestamp + (fraction[0] * pow(2, -64))
        unix_val = datetime.utcfromtimestamp(time)
        
        data5 = input_file.read(4)
        metric_array_size =struct.unpack(">I", data5)
        m_array_size = metric_array_size[0]
        
        data6=input_file.read(4*m_array_size)
        x=">"+str(m_array_size)+"f"
        metrics_array =struct.unpack(x, data6)
    
        data7= input_file.read(4)
        image_num_row= struct.unpack(">I", data7)
    
        data8= input_file.read(4)
        image_num_col= struct.unpack(">I", data8)
        
        image_array= np.empty(shape=(image_num_row[0], image_num_col[0]), dtype=int)
        for i in range(0, image_num_row[0]):
            for j in range(0, image_num_col[0]):
                data=input_file.read(1)
                image_array[i,j] = struct.unpack(">B", data)[0]                #Read one byte at a time and place into a 2d array -> creates the image once plotted
        print("Image for Record: " + str(n))
        plt.imshow(image_array, interpolation='nearest')
        plt.gray()                                                             #Required for the plot to use grayscale rather than a heatmap looking style
        plt.show()    
        print("--------------------------------------------------")
        lst.append([n, frame_num[0], ms_time[0], unix_val, metrics_array[0], metrics_array[1], metrics_array[2], metrics_array[3], metrics_array[4],metrics_array[5],
                   metrics_array[6],metrics_array[7],metrics_array[8],metrics_array[9],metrics_array[10],metrics_array[11],metrics_array[12],metrics_array[13],metrics_array[14]
                   ,metrics_array[15],metrics_array[16],metrics_array[17],metrics_array[18],metrics_array[19],metrics_array[20],metrics_array[21],metrics_array[22],metrics_array[23],
                   metrics_array[24],metrics_array[25],metrics_array[26],metrics_array[27],metrics_array[28],metrics_array[29],metrics_array[30],metrics_array[31],metrics_array[32],
                   metrics_array[33],metrics_array[34],metrics_array[35]])
        
    df1 = pd.DataFrame(lst, columns=cols)   
    return df1
        

def ImageSelector(file, s,f, output):
    """
    Saves images for the deisred records

    Parameters
    ----------
    file : Str
        The input file.
    s : Int
        The first record.
    f : Int
        The final record.

    Returns
    -------
    None.
    
    Outputs
    -------
    .png images
    """
    
    import matplotlib.pyplot as plt
    plt.gray()
    plt.ioff()
    from matplotlib import pyplot as plt
    import numpy as np
    import struct
    import os
    input_file_name = (file)

    input_file = open(input_file_name, 'rb')
    data = input_file.read(1)
    data1 = input_file.read(16)
    header = struct.unpack(">4i", data1)
    
    input_file.seek(header[3]*s, 1)
    
    from tqdm import tqdm
    for n in tqdm(range(s, f)):
        
        input_file.read(24)
        
        data5 = input_file.read(4)
        metric_array_size =struct.unpack(">I", data5)
        m_array_size = metric_array_size[0]

        input_file.read(4*m_array_size)

        data7= input_file.read(4)
        image_num_row= struct.unpack(">I", data7)

        data8= input_file.read(4)
        image_num_col= struct.unpack(">I", data8)

        image_array= np.empty(shape=(image_num_row[0], image_num_col[0]), dtype=int)
        for i in range(0, image_num_row[0]):
            for j in range(0, image_num_col[0]):
                data=input_file.read(1)
                image_array[i,j] = struct.unpack(">B", data)[0]
    
        plt.imshow(image_array, interpolation='nearest')
        name="image"+str(n)+".png"
        plt.savefig(os.path.join(output, name))
        plt.close()
        #plt.show()

#A function to output the .movr file details (excluding the 2d image array) into a csv file
def MovrToCSV(file,output):
    """

    Parameters
    ----------
    file : Str
        Input .movr file.
    output : Str
        Desired output file .csv location.

    Returns
    -------
    None.
    
    Outputs
    -------
    CSV file
    """
    
    import numpy as np
    import pandas as pd
    import struct
    from datetime import datetime
    input_file_name = (file)
    
    input_file = open(input_file_name, 'rb')
    data = input_file.read(1)
    data1 = input_file.read(16)
    header = struct.unpack(">4i", data1)
    header_length= input_file.tell()
    
    
    cols = ['Record Number', 'Frame Number', 'Timestamp (ms)', 'DateTime', 'Error_code', 'Areapix', 'cXpix', 'cYpix',
           'Orientation','Top_pix','Bounding_Diag','Axis_X1','Axis_Y1','Axis_X2','Axis_Y2','cXmm','cX','cYmm','cY',
           'Top_mm','Vx_mm_per_sec','Vy_mm_per_sec','Orbital_deg','Orbital_radius','Orbital_deg_per_sec','Noise_level','Vx_Av_mm_per_sec','Vy_Av_mm_per_sec','W_Av_deg_per_sec',
           'Track_deg','Speed_mm_per_sec','Speed_Av_mm_per_sec','dXmm','dYmm','distance_mm','Heading_deg','HeadingConf','Length','HeadX_pix','HeadY_pix']
    lst = []
    
    #reading bytes?
    import os
    size = os.path.getsize(input_file_name)
    s = size - header_length
    record_length = s/header[3]
    
    from tqdm import tqdm
    for n in tqdm(range(0,int(record_length))):
        
        data2 = input_file.read(4)
        frame_num = struct.unpack(">I", data2)
        
        data3 = input_file.read(4)
        ms_time = struct.unpack(">I", data3)
        
        data4 = input_file.read(8)
        ab_time = struct.unpack(">q", data4)
        timestamp = ab_time[0]-2082816000
       
        data4b=input_file.read(8)
        fraction = struct.unpack(">Q", data4b)
        time = timestamp +(fraction[0] * pow(2, -64))
        unix_val = datetime.utcfromtimestamp(time)
            
        data5 = input_file.read(4)
        metric_array_size =struct.unpack(">I", data5)
        m_array_size = metric_array_size[0]
        
        data6=input_file.read(4*m_array_size)
        x=">"+str(m_array_size)+"f"
        metrics_array =struct.unpack(x, data6)
    
        data7= input_file.read(4)
        image_num_row= struct.unpack(">I", data7)
    
        data8= input_file.read(4)
        image_num_col= struct.unpack(">I", data8)
        
        image_array= np.empty(shape=(image_num_row[0], image_num_col[0]), dtype=int)
        for i in range(0, image_num_row[0]):
            for j in range(0, image_num_col[0]):
                data=input_file.read(1)
                image_array[i,j] = struct.unpack(">B", data)[0]  
            
        lst.append([n, frame_num[0], ms_time[0], unix_val, metrics_array[0], metrics_array[1], metrics_array[2], metrics_array[3], metrics_array[4],metrics_array[5],
                   metrics_array[6],metrics_array[7],metrics_array[8],metrics_array[9],metrics_array[10],metrics_array[11],metrics_array[12],metrics_array[13],metrics_array[14]
                   ,metrics_array[15],metrics_array[16],metrics_array[17],metrics_array[18],metrics_array[19],metrics_array[20],metrics_array[21],metrics_array[22],metrics_array[23],
                   metrics_array[24],metrics_array[25],metrics_array[26],metrics_array[27],metrics_array[28],metrics_array[29],metrics_array[30],metrics_array[31],metrics_array[32],
                   metrics_array[33],metrics_array[34],metrics_array[35]])
        
    df1 = pd.DataFrame(lst, columns=cols)
    df1.to_csv(output)


#A function to extract and print the Index file header
def IndexHeader(file, Video=1):
    """
    Function to read and output the index file header
    Parameters
    ----------
    file : str
        Input .idx file.
    Video : int (0 or 1)
        To say if you had created movr files when doing the experiment. 
        Default is yes (1). If you hadnt, use (0)
    Returns
    -------
    df1 : DataFrame
        A dataframe containing index file header information.

    """
    
    import struct
    from datetime import datetime
    import pandas as pd
    input_file_name = (file)
    input_file = open(input_file_name, 'rb')

    print("Header:")
    data = input_file.read(1)
    filetype_version = struct.unpack(">B", data)
    print('The filetype version is:       '+str(filetype_version[0]))

    data1=input_file.read(4)
    metrics_list_array_size=struct.unpack(">I", data1)
    print('The metrics list array size:   '+str(metrics_list_array_size[0]))

    data2=input_file.read(2*metrics_list_array_size[0])
    mla=">"+str(metrics_list_array_size[0])+"H"
    metrics_list_array=struct.unpack(mla, data2)
    print('The metrics list array:        '+str(metrics_list_array))

    data3=input_file.read(4)
    record_size=struct.unpack(">i",data3)
    print('The record size:               '+str(record_size[0]))

    if Video==1:    
        xx=0  
        while (byte := input_file.read(1)): 
            xx=xx+1#The while is to skip past the next few bytes until it finds the .movr bytes
            if b'.' in byte:
                byte = input_file.read(4)
                xx=xx+4
                if byte==b'movr':
                    break
                else:
                    continue
            else:
                continue
    elif Video==0:
        xx=0  
        while (byte := input_file.read(1)): 
            xx=xx+1#The while is to skip past the next few bytes until it finds the .movr bytes
            if b'V' in byte:
                byte = input_file.read(3)
                xx=xx+3
                if byte==b'OID':
                    break
                else:
                    continue
            else:
                continue
        
    data4 = input_file.read(8)
    ab_time = struct.unpack(">q", data4)
    timestamp = ab_time[0]-2082816000
    data4b=input_file.read(8)
    fraction = struct.unpack(">Q", data4b)
    time = timestamp + (fraction[0] * pow(2, -64))
    unix_val = datetime.utcfromtimestamp(time)
    
    print('The absolute timestamp is:     '+str(ab_time[0]))
    print('The fraction is:               '+str(fraction[0]))
    print('The unix time is:              '+str(timestamp))  
    print("DateTime:                     ",unix_val)

    data5=input_file.read(4)
    group_string_length = struct.unpack(">I", data5)
    print("The group string length:       "+str(group_string_length[0]))

    input_file.read(group_string_length[0])
    if group_string_length[0] > 0:
        group_string=struct.unpack(">c", data5)
        print(group_string)
        
    #reading bytes?
    import os
    size = os.path.getsize(input_file_name)
    print("The total size is:             " +str(size))
    s = size -(77+(2*metrics_list_array_size[0])+(group_string_length[0])+xx)   #Not sure if the xx will work for all cases.. in this case is 69
    print("The size minus header:         " +str(s))
    record_length = s/record_size[0]
    print("The number of records is:      "+str(record_length))
    print("------------------------------------------------") 
    metrics=['Error_code', 'Areapix', 'cXpix', 'cYpix',
           'Orientation','Top_pix','Bounding_Diag','Axis_X1','Axis_Y1','Axis_X2','Axis_Y2','cXmm','cX','cYmm','cY',
           'Top_mm','Vx_mm_per_sec','Vy_mm_per_sec','Orbital_deg','Orbital_radius','Orbital_deg_per_sec','Noise_level','Vx_Av_mm_per_sec','Vy_Av_mm_per_sec','W_Av_deg_per_sec',
           'Track_deg','Speed_mm_per_sec','Speed_Av_mm_per_sec','dXmm','dYmm','distance_mm','Heading_deg','HeadingConf','Length','HeadX_pix','HeadY_pix']
    m1=metrics[(metrics_list_array[0])]
    m2=metrics[(metrics_list_array[1])]
    m3=metrics[(metrics_list_array[2])]
    m4=metrics[(metrics_list_array[3])]
    m5=metrics[(metrics_list_array[4])]
    cols = ['Filetype_Version', 'DateTime', 'Record_Size', 'Number_of_Records', 'Metric1', 'Metric2', 'Metric3', 'Metric4', 'Metric5']
    lst = []
    lst.append([filetype_version[0], unix_val, record_size[0],  record_length, m1, m2, m3,m4,m5])
    df1 = pd.DataFrame(lst, columns=cols)
    return df1    

def HeaderVariables(file, Video=1):
    """
    Function to read and output the index file header
    Parameters
    ----------
    file : str
        Input .idx file.
    Video : int (0 or 1)
        To say if you had created movr files when doing the experiment. 
        Default is yes (1). If you hadnt, use (0)
    Returns
    -------
    df1 : DataFrame
        A dataframe containing index file header information.

    """
    
    import struct
    input_file_name = (file)
    input_file = open(input_file_name, 'rb')

    input_file.read(1)

    data1=input_file.read(4)
    metrics_list_array_size=struct.unpack(">I", data1)

    input_file.read(2*metrics_list_array_size[0])

    data3=input_file.read(4)
    record_size=struct.unpack(">i",data3)


    if Video==1:    
        xx=0  
        while (byte := input_file.read(1)): 
            xx=xx+1#The while is to skip past the next few bytes until it finds the .movr bytes
            if b'.' in byte:
                byte = input_file.read(4)
                xx=xx+4
                if byte==b'movr':
                    break
                else:
                    continue
            else:
                continue
    elif Video==0:
        xx=0  
        while (byte := input_file.read(1)): 
            xx=xx+1#The while is to skip past the next few bytes until it finds the .movr bytes
            if b'V' in byte:
                byte = input_file.read(3)
                xx=xx+3
                if byte==b'OID':
                    break
                else:
                    continue
            else:
                continue
        
    input_file.read(8)

    input_file.read(8)


    data5=input_file.read(4)
    group_string_length = struct.unpack(">I", data5)

    input_file.read(group_string_length[0])
    if group_string_length[0] > 0:
        group_string=struct.unpack(">c", data5)
        print(group_string)

    headlen=(77+(2*metrics_list_array_size[0])+(group_string_length[0])+xx)
    return headlen, record_size[0]

def IndexRecordSelector(file,start,f, Video=1):
    """
    A function to extract and print the desired records from the index file
    
    Parameters
    ----------
    file : Str
        Input .idx file.
    start : Int
        Start frame.
    f : Int
        End frame.
    Video : int (0 or 1)
        To say if you had created movr files when doing the experiment. 
        Default is yes (1). If you hadnt, use (0)
    Returns
    -------
    df1 : DataFrame
        Output dataframe with each row as a record/frame from the index file.

    """
    
    #INDEX FILE
    import struct
    from datetime import datetime
    import pandas as pd
    input_file_name = (file)
    input_file = open(input_file_name, 'rb')
    
    print("Header:")
    data = input_file.read(1)
    filetype_version = struct.unpack(">B", data)
    print('The filetype version is:       '+str(filetype_version[0]))
    
    data1=input_file.read(4)
    metrics_list_array_size=struct.unpack(">I", data1)
    print('The metrics list array size:   '+str(metrics_list_array_size[0]))
    
    data2=input_file.read(2*metrics_list_array_size[0])
    mla=">"+str(metrics_list_array_size[0])+"H"
    metrics_list_array=struct.unpack(mla, data2)
    print('The metrics list array:        '+str(metrics_list_array))
    
    data3=input_file.read(4)
    record_size=struct.unpack(">i",data3)
    print('The record size:               '+str(record_size[0]))
    
    if Video==1:    
        xx=0  
        while (byte := input_file.read(1)): 
            xx=xx+1#The while is to skip past the next few bytes until it finds the .movr bytes
            if b'.' in byte:
                byte = input_file.read(4)
                xx=xx+4
                if byte==b'movr':
                    break
                else:
                    continue
            else:
                continue
    elif Video==0:
        xx=0  
        while (byte := input_file.read(1)): 
            xx=xx+1#The while is to skip past the next few bytes until it finds the .movr bytes
            if b'V' in byte:
                byte = input_file.read(3)
                xx=xx+3
                if byte==b'OID':
                    break
                else:
                    continue
            else:
                continue
    data4 = input_file.read(8)
    ab_time = struct.unpack(">q", data4)
    timestamp = ab_time[0]-2082816000
    data4b=input_file.read(8)
    fraction = struct.unpack(">Q", data4b)
    time = timestamp + (fraction[0] * pow(2, -64))
    unix_val = datetime.utcfromtimestamp(time)  
    print("DateTime:                     ",unix_val)
    
    data5=input_file.read(4)
    group_string_length = struct.unpack(">I", data5)
    print("The group string length:       "+str(group_string_length[0]))
    
    input_file.read(group_string_length[0])
    if group_string_length[0] > 0:
        group_string=struct.unpack(">c", data5)
        print(group_string)
    data7=input_file.read(48)
    
    
    #reading bytes?
    import os
    size = os.path.getsize(input_file_name)
    print("The total size is:             " +str(size))
    s = size -(77+(2*metrics_list_array_size[0])+(group_string_length[0])+xx)   #Not sure if the xx will work for all cases.. in this case is 69
    print("The size minus header:         " +str(s))
    record_length = s/record_size[0]
    print("The number of records is:      "+str(record_length))
    
    print("------------------------------------------------")
    input_file.seek(record_size[0]*start, 1)
    
    cols = ['Record Number', 'Timestamp (ms)', 'State', 'Activity Level', 'Movr Frame', 'cXmm', 'Speed_Av_mm_per_sec', 'Heading_deg', 'cYmm', 'Error_code'] #Will need to change the metric names if they change
    lst = []
    
    for n in range(start,f):
        
        data7=input_file.read(4)
        ms_time=struct.unpack(">I", data7)
        
        data8=input_file.read(1)
        state=struct.unpack(">B",data8)
        if state[0] == 0:
            x="Unknown"
        elif state[0] == 1:
            x="Locomotive"
        elif state[0] == 2:
            x="Stationary"
        elif state[0]== 3:
            x="Stationary Static"
        elif state[0]==4:
            x="Stationary Active"
        
        data9 = input_file.read(2)
        activity_level=struct.unpack(">H",data9)
        
        data10 = input_file.read(4)
        movr_frame=struct.unpack(">I", data10)
        
        data11 = input_file.read(4)
        metrics_array_size=struct.unpack(">I", data11)
        
        data12 = input_file.read(4*metrics_array_size[0])
        a =">"+str(metrics_array_size[0])+"f"
        metrics_array=struct.unpack(a, data12)
        lst.append([n, ms_time[0], x, activity_level[0], movr_frame[0], metrics_array[0], metrics_array[1], metrics_array[2], metrics_array[3], metrics_array[4]])
    df1 = pd.DataFrame(lst, columns=cols)
    return df1
        
def IndexToCSV(file,output, Video=1):
    """
    A function to convert the whole index file (excluding the header) to a csv

    Parameters
    ----------
    file : Str
        Input .idx file location
    output : Str
        Output .csv file location  
    Video : int (0 or 1)
        To say if you had created movr files when doing the experiment. 
        Default is yes (1). If you hadnt, use (0)
    Returns
    -------
    None.
    
    Outputs
    -------
    CSV
    """
    
    import struct
    import pandas as pd
    input_file_name = (file)
    input_file = open(input_file_name, 'rb')

    input_file.read(1)
    data1=input_file.read(4)
    metrics_list_array_size=struct.unpack(">I", data1)
    input_file.read(2*metrics_list_array_size[0])
    data3=input_file.read(4)
    record_size=struct.unpack(">i",data3)

    if Video==1:    
        xx=0  
        while (byte := input_file.read(1)): 
            xx=xx+1#The while is to skip past the next few bytes until it finds the .movr bytes
            if b'.' in byte:
                byte = input_file.read(4)
                xx=xx+4
                if byte==b'movr':
                    break
                else:
                    continue
            else:
                continue
    elif Video==0:
        xx=0  
        while (byte := input_file.read(1)): 
            xx=xx+1#The while is to skip past the next few bytes until it finds the .movr bytes
            if b'V' in byte:
                byte = input_file.read(3)
                xx=xx+3
                if byte==b'OID':
                    break
                else:
                    continue
            else:
                continue
    input_file.read(8)
    input_file.read(8)
    data5=input_file.read(4)
    group_string_length = struct.unpack(">I", data5)

    input_file.read(group_string_length[0])
    if group_string_length[0] > 0:
        group_string=struct.unpack(">c", data5)
        print(group_string)
    data7=input_file.read(48)


    #reading bytes?
    import os
    size = os.path.getsize(input_file_name)
    s = size -(77+(2*metrics_list_array_size[0])+(group_string_length[0])+xx)   #Not sure if the xx will work for all cases.. in this case is 69
    record_length = s/record_size[0]

    cols = ['Record Number', 'Timestamp (ms)', 'State', 'Activity Level', 'Movr Frame', 'cXmm', 'Speed_Av_mm_per_sec', 'Heading_deg', 'cYmm', 'Error_code'] #Will need to change the metric names if they change
    lst = []
    
    from tqdm import tqdm
    for n in tqdm(range(0,int(record_length))):
        data7=input_file.read(4)
        ms_time=struct.unpack(">I", data7)

        data8=input_file.read(1)
        state=struct.unpack(">B",data8)
        if state[0] == 0:
            x="Unknown"
        elif state[0] == 1:
            x="Locomotive"
        elif state[0] == 2:
            x="Stationary"
        elif state[0]== 3:
            x="Stationary Static"
        elif state[0]==4:
            x="Stationary Active"

        data9 = input_file.read(2)
        activity_level=struct.unpack(">H",data9)

        data10 = input_file.read(4)
        movr_frame=struct.unpack(">I", data10)

        data11 = input_file.read(4)
        metrics_array_size=struct.unpack(">I", data11)

        data12 = input_file.read(4*metrics_array_size[0])
        a =">"+str(metrics_array_size[0])+"f"
        metrics_array=struct.unpack(a, data12)
        lst.append([n, ms_time[0], x, activity_level[0], movr_frame[0], metrics_array[0], metrics_array[1], metrics_array[2], metrics_array[3], metrics_array[4]])

    df1 = pd.DataFrame(lst, columns=cols)
    df1.to_csv(output)

def csv_read(file, fps=45, ZT=None):
    """
    Reading and adjusting csv input

    Parameters
    ----------
    file : Str
        Input .csv file

    Returns
    -------
    df1 : DataFrame
        Outputs a dataframe with additional columns from the .csv input

    """
    import pandas as pd
    import numpy as np
    df = pd.read_csv(file)
    df['Time_ms'] = df['Timestamp (ms)'] - df.loc[0,'Timestamp (ms)']
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df1 = df.copy()

    #Separates each bout of state. The 'bout' column provides the number corresponding to the bout.
    df1['State_before'] = df1["State"].shift(1)
    df1['State_after']=df1["State"].shift(-1)
    df1["e4"] = df1["State"] != df1["State_before"]
    df1["Bout"] = df1["e4"].cumsum()
    df1["e6"] = df1.Time_ms.shift(-1)   #<-This provides the time from the row below
    
    #Showing the frame & time for each bout of a state
    df1['Bout_frame_number'] = df1.groupby('Bout').cumcount()
    df1['bd']  = df1.Time_ms - df1.Time_ms.shift(1).fillna(0)
    df1.loc[((df1['Bout_frame_number']==0)), ['bd']] = 100
    df1['Bout_duration'] = df1.groupby('Bout')['bd'].cumsum()
    df1['Hour'] = df1['Time_ms']/3600000
    df1['Minutes'] = df1['Hour']*60
    df1['Seconds'] = df1['Minutes'] * 60
    
    df1.loc[(df1['State']=='Locomotive'), ['State Number']] = 2
    df1.loc[(df1['State']=='Stationary Active'), ['State Number']] = 1
    df1.loc[(df1['State']=='Stationary Static'), ['State Number']] = 0
    
    df1['DistanceTravelled'] = np.sqrt((abs(df1['cYmm'] - df1['cYmm'].shift(1))**2) +(abs(df1['cXmm'] - df1['cXmm'].shift(1))**2)).fillna(0)
    if ZT != None:
        df1['ZT'] = df1['Hour'] + ZT
        for a in [24,48,72]:
            df1.loc[((df1['ZT']>=a) & (df1['ZT']<a+24)), ['ZT']] = df1['ZT'] - a
        df1.loc[((df1['ZT']>=0) & (df1['ZT']<12)), ['TOD']] = 'Day'
        df1.loc[((df1['ZT']>=12) & (df1['ZT']<24)), ['TOD']] = 'Night'
    else:
        df1['ZT']= np.NaN
        df1['TOD']= np.NaN
    
    cols=['Record Number','Movr Frame','Error_code','Timestamp (ms)','Time_ms','Seconds','Minutes','Hour','ZT','TOD','State_before','State','State Number','State_after',"e6",'Bout','Bout_frame_number','Bout_duration',
      'Activity Level', 'Speed_Av_mm_per_sec', 'cXmm', 'cYmm', 'DistanceTravelled','Heading_deg']
    df1 = df1[cols]
    return df1

def thresholder(df,frames):
    test=df.loc[:,['Time_ms','State']].copy()
    for n in range(1,frames):
        test['State+'+str(n)]=test["State"].shift(-(n)).fillna('Locomotive')
        test['State-'+str(n)]=test["State"].shift(n).fillna('Locomotive')
    
    test['PreLO'] =test.loc[:, [col for col in test.columns if 'State-' in col]].isin({'Locomotive'}).sum(1)
    test['PreSA'] =test.loc[:, [col for col in test.columns if 'State-' in col]].isin({'Stationary Active'}).sum(1)
    test['PreSS'] =test.loc[:, [col for col in test.columns if 'State-' in col]].isin({'Stationary Static'}).sum(1)
    test['PostLO'] =test.loc[:, [col for col in test.columns if 'State+' in col]].isin({'Locomotive'}).sum(1)
    test['PostSA'] =test.loc[:, [col for col in test.columns if 'State+' in col]].isin({'Stationary Active'}).sum(1)
    test['PostSS'] =test.loc[:, [col for col in test.columns if 'State+' in col]].isin({'Stationary Static'}).sum(1)
    test['New State']=test['State']
    test.loc[((test['State']=='Stationary Active')&(test['PostSS']>=frames/2)&(test['PreSA']<=frames/2)), ['New State']] = 'Stationary Static'
    test.loc[((test['State']=='Stationary Active')&(test['PostLO']>=frames/2)&(test['PreSA']<=frames/2)), ['New State']] = 'Locomotive'
    test.loc[((test['State']=='Stationary Static')&(test['PostSA']>=frames/2)&(test['PreSA']>=frames/2)), ['New State']] = 'Stationary Active'
    test.loc[((test['State']=='Locomotive')&(test['PostSA']>=frames/2)&(test['PreSA']>=frames/2)), ['New State']] = 'Stationary Active'

    test['State_before'] = test["State"].shift(1)
    test["e4"] = test["State"] != test["State_before"]
    test["Bout"] = test["e4"].cumsum()
    test["Next Time"] = test.Time_ms.shift(-1)   #<-This provides the time from the row below

    test['New State_before'] = test["New State"].shift(1)
    test["e4"] = test["New State"] != test["New State_before"]
    test["New Bout"] = test["e4"].cumsum()

    df['State']= test['New State']
    df['Bout'] = test["New Bout"]
    return df
    
def XYH(dfi, tt=1,inverted=False):
    df2_gbmax = dfi.groupby(['Bout', 'State', 'Fly'])[['e6']].max()
    df2_gbmin = dfi.groupby(['Bout', 'State', 'Fly'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3['Seconds'] = df3['Time']/1000
    df3['TOD'] = dfi.groupby(['Bout', 'State'])[['TOD']].nth(0)  
    df3['sX'] = dfi.groupby(['Bout', 'State'])[['cXmm']].nth(0)  
    df3['eX'] = dfi.groupby(['Bout', 'State'])[['cXmm']].nth(-1) 
    df3['minX'] = dfi.groupby(['Bout', 'State'])[['cXmm']].min()
    df3['maxX'] = dfi.groupby(['Bout', 'State'])[['cXmm']].max()
    df3['meanX'] = dfi.groupby(['Bout', 'State'])[['cXmm']].mean()
    df3['sY'] = dfi.groupby(['Bout', 'State'])[['cYmm']].nth(0)
    df3['eY'] = dfi.groupby(['Bout', 'State'])[['cYmm']].nth(-1)
    df3['minY'] = dfi.groupby(['Bout', 'State'])[['cYmm']].min()
    df3['maxY'] = dfi.groupby(['Bout', 'State'])[['cYmm']].max()
    df3['meanY'] = dfi.groupby(['Bout', 'State'])[['cYmm']].mean()
    df3['sH'] = dfi.groupby(['Bout', 'State'])[['Heading_deg']].nth(0)
    df3['eH'] = dfi.groupby(['Bout', 'State'])[['Heading_deg']].nth(-1)
    df3['minH'] = dfi.groupby(['Bout', 'State'])[['Heading_deg']].min()
    df3['maxH'] = dfi.groupby(['Bout', 'State'])[['Heading_deg']].max()
    df3['meanH'] = dfi.groupby(['Bout', 'State'])[['Heading_deg']].mean()
    df3['meanSpeed'] = dfi.groupby(['Bout', 'State'])[['Speed_Av_mm_per_sec']].mean()
    df3['meanAL'] = dfi.groupby(['Bout', 'State'])[['Activity Level']].mean()
    df3['ZT'] = dfi.groupby(['Bout', 'State'])[['ZT']].nth(0)
    df=df3.reset_index()
    df = df[df['Seconds'] >= tt]
    df.loc[((df['sY']>=1.9)), ['Location']] = 'Ground'
    df.loc[((df['sY']<1.9)), ['Location']] = 'Ceiling'
    df['Fly'] = dfi.loc[0,'Fly']
    df.loc[(df['sH'] < 90), ['sH']] = df.loc[(df['sH'] < 90), ['sH']] +360
    df.loc[(df['eH'] < 90), ['eH']] = df.loc[(df['eH'] < 90), ['eH']] +360
    df.loc[(df['minH'] < 90), ['minH']] = df.loc[(df['minH'] < 90), ['minH']] +360
    df.loc[(df['maxH'] < 90), ['maxH']] = df.loc[(df['maxH'] < 90), ['maxH']] +360
    df.loc[(df['meanH'] < 90), ['meanH']] = df.loc[(df['meanH'] < 90), ['meanH']] +360
    if inverted==True:
        df['X'] = 65 - df['X']
        df['sX'] = 65 - df['sX'] 
        df['eX'] = 65 - df['eX']
        df['minX'] = 65 - df['minX']
        df['maxX'] = 65 - df['maxX'] 
        df['meanX'] = 65 - df['meanX']
        return df
    else:
        return df

def XYH_setup(path):
    import os
    import pandas as pd
    dfs=[]
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in [f for f in filenames if f=="XYH.csv"]:
            df=pd.read_csv(os.path.join(dirpath, filename))
            dfs.append(df)
    df=pd.concat(dfs)
    df['e6'] = df['Fly'].shift(1)
    df['e6'] = df['e6'].fillna(0)
    df["e7"] = ((df["Fly"] > df["e6"]) | ((df["Fly"]==0) & (df["e6"]!=0)))
    df["e8"] = df["e7"].cumsum()
    df['dsY'] =  3.5 - df['sY']
    df['Y_av'] = ((df['sY'] +df['eY'])/2) 
    return df



def cY_cHead(dfi,tt,tod='all',state='ss'):
    import pandas as pd
    df2_gbmax = dfi.groupby(['Bout', 'State'])[['e6']].max() 
    df2_gbmin = dfi.groupby(['Bout', 'State'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df = dfi.groupby(['Bout', 'State'])[['Heading_deg']].nth(0)
    df3['Heading'] = df['Heading_deg']
    df = dfi.groupby(['Bout', 'State'])[['cYmm']].nth(0)
    df3['Y'] = df['cYmm']
    df3=df3.reset_index()
    
    if type(tt) ==int:
        df3 = df3[df3['Time']>=tt]
    elif type(tt) ==list:
        df3 = df3[(df3['Time']>=tt[0]) & (df3['Time']<tt[1])]
    else:
        raise ValueError('Use a single time threshold eg. 3000, or provide two numbers eg. [0,100]')
        
    if state.lower() == 'ss' or state.lower() == 'stationary static':
        df3 = df3[df3['State'].isin(['Stationary Static'])]
    elif state.lower() == 'sa' or state.lower() == 'stationary active':
        df3 = df3[df3['State'].isin(['Stationary Active'])] 
    elif state.lower() == 'lo' or state.lower() == 'locomotive':
        df3 = df3[df3['State'].isin(['Locomotive'])]
    else:
        raise ValueError('Select a state')
        
    if tod.lower()=='all':
        df3=df3
    elif tod.lower()=='day':
        df3 = df3[df3['TOD'] =='Day']
    
    elif tod.lower()=='night':
        df3 = df3[df3['TOD'] =='Night']
    else:
        raise ValueError('Select a time of day - day or night or all')    
        
    BoutList = df3['Bout'].tolist()
    df1 = dfi.loc[:, ['Fly','Bout', 'TOD','cYmm', 'Bout_frame_number', 'Bout_duration',  "Heading_deg"]]
    df = df1.query('Bout in @BoutList')
    df.loc[(df['Heading_deg'] < 90), ['Heading_deg']] = df.loc[(df['Heading_deg'] < 90), ['Heading_deg']] +360  
    dfi=df.copy()
    h = dfi.groupby(['Bout'])[['Heading_deg']].min().reset_index()
    hmax = dfi.groupby(['Bout'])[['Heading_deg']].max().reset_index()
    h.rename(columns={'Heading_deg':'Min'}, inplace=True)
    h['Max'] = hmax['Heading_deg']
    h['Diff'] = h['Max'] - h['Min']
    Keep = h[h['Diff']<50]
    BoutList = Keep['Bout'].tolist()
    dfi = dfi.query('Bout in @BoutList').copy()


    df3 = dfi.groupby(['Bout'])[['Heading_deg']].nth(0)
    df = dfi.groupby(['Bout'])[['cYmm']].nth(0)
    df3['cYmm'] = df['cYmm']
    dft_cY=df3.reset_index()
    
    e5_list = dft_cY['Bout'].tolist()
    cHead_list = dft_cY['Heading_deg'].tolist()
    cYmm_list =  dft_cY['cYmm'].tolist()

    data = pd.DataFrame()
    for (a, b,c) in zip(e5_list, cHead_list,cYmm_list):
        df = dfi[dfi['Bout'] ==a].copy()
        if b < 270:
            df['Heading'] = df['Heading_deg'] - b
        else:
            df['Heading'] = -(df['Heading_deg'] -b)
            
        if c>=1.9:
            df['Ypos']='Ground'
        else:
            df['Ypos']='Ceiling'
        df['Y'] = df['cYmm'] - c
        data = pd.concat([data, df], ignore_index=True)

    return data


def cY_cHead_setup(df):
    
    y = df.groupby(['Bout'])['Y'].nth(3).reset_index()
    BoutList = y[y['Y']!=0.0]['Bout'].to_list()
    df = df.query('Bout in @BoutList').copy()
    
    df['S'] = df['Bout_duration']/1000
    df['M'] = df['S']/60
    df_b_av = df.groupby(['Bout_frame_number','S', 'M'])[['Heading']].mean()
    df_b_av = df_b_av.reset_index()
    df_b_av['deltaHeading'] = df_b_av['Heading'] - (df_b_av.loc[0,'Heading'])
    df1 = df.groupby(['Bout_frame_number'])[['Heading']].sem()
    df1 = df1.reset_index()
    df_b_av['dHeadingSEM'] = df1['Heading']
    df_b_av['dHeadingSEM'] = df_b_av['dHeadingSEM'] -df_b_av.loc[0,'dHeadingSEM']
    df_b_av['dHci'] = df_b_av['dHeadingSEM']*1.96 
    
    df_ss = df.groupby(['Bout_frame_number','S', 'M'])[['Heading']].count()
    df_ss = df_ss.reset_index()
    df_b_av['Sample Size'] = df_ss['Heading']
    
    df1 = df.groupby(['Bout_frame_number','S', 'M'])[['Y']].mean()
    df1 = df1.reset_index()
    df_b_av['Y'] = df1['Y']
    df_b_av['deltaY'] = df_b_av['Y'] - (df_b_av.loc[0,'Y'])

    df1 = df.groupby(['Bout_frame_number'])[['Y']].sem()
    df1 = df1.reset_index()
    df_b_av['dYSEM'] = df1['Y']
    df_b_av['dYSEM'] = df_b_av['dYSEM'] -df_b_av.loc[0,'dYSEM']
    df_b_av['dYci'] = df_b_av['dYSEM']*1.96 
    return df_b_av
    

        
def cYcH_prerest(dfi, tt):
    import pandas as pd
    fps = (1000/dfi.loc[0,'Bout_duration'])
    dfi=dfi.loc[:,["Time_ms","Record Number","State",  "cYmm",  "Heading_deg", "Bout", "e6"]]
    dfi.loc[(dfi['Heading_deg'] < 90), ['Heading_deg']] = dfi.loc[(dfi['Heading_deg'] < 90), ['Heading_deg']] +360
    df2_gbmax = dfi.groupby(['Bout', 'State'])[['e6']].max() 
    df2_gbmin = dfi.groupby(['Bout', 'State'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3['Start_frame'] = dfi.groupby(['Bout', 'State'])[['Record Number']].min() 
    df3['End_frame'] = dfi.groupby(['Bout', 'State'])[['Record Number']].max() 
    df3['Hdiff'] = dfi.groupby(['Bout', 'State'])[['Heading_deg']].max() -dfi.groupby(['Bout', 'State'])[['Heading_deg']].min() 
    df3['Ydiff'] = dfi.groupby(['Bout', 'State'])[['cYmm']].max() -dfi.groupby(['Bout', 'State'])[['cYmm']].min() 

    df3 = df3.reset_index()
    df3 = df3[(df3['State'] =='Stationary Static') & (df3['Hdiff'] <50) & (df3['Ydiff'] !=0)]
    if type(tt) ==int:
        df3 = df3[df3['Time']>=tt]
    elif type(tt) ==list:
        df3 = df3[(df3['Time']>=tt[0]) & (df3['Time']<tt[1])]
    else:
        raise ValueError('Use a single time threshold eg. 3000, or provide two numbers eg. [0,100]')
        
    if len(df3)>=1:
        df3['SL_90'] = df3['Start_frame'] - (2*fps)
        SL = df3['SL_90'].tolist()
        EL = df3['End_frame'].tolist()   
        NM = df3['Bout'].tolist()
        data = pd.DataFrame()
        for (a, b, c) in zip(SL, EL, NM):
                df = dfi.loc[a:b,].copy()
                df['new_e5'] = c
                StartY, StartH = df['cYmm'].iloc[0], df['Heading_deg'].iloc[0]
                if StartY>=1.9:
                    df['Position'] = 'Ground'
                else:
                    df['Position'] = 'Ceiling'
                df['Y'] = df['cYmm'] - StartY
                
                if StartH < 270:
                    df['Heading'] = df['Heading_deg'] - StartH
                else:
                    df['Heading'] = -(df['Heading_deg'] -StartH)
                data = pd.concat([data, df], ignore_index=True)
        data['new_bout_frame_number'] = data.groupby('new_e5').cumcount()
        data['new_bout_duration_rough'] = (data['new_bout_frame_number'] * ((1/fps)*1000)) + ((1/fps)*1000)
        return data
    else:
        data = pd.DataFrame()
        return data      

def PreRest_setup(df):
    
    y = df.groupby(['new_e5'])['Y'].nth(3).reset_index()
    BoutList = y[y['Y']!=0.0]['new_e5'].to_list()
    df = df.query('new_e5 in @BoutList').copy()
    
    df['S'] = df['new_bout_duration_rough']/1000
    df['M'] = df['S']/60
    df_b_av1 = df.groupby(['new_bout_frame_number','S', 'M'])[['Y']].mean().reset_index()
    df_b_av1['deltaY'] = df_b_av1['Y'] - (df_b_av1.loc[0,'Y'])
    df1 = df.groupby(['new_bout_frame_number'])[['Y']].sem().reset_index()
    df_b_av1['dYci'] = df1['Y']*1.96
    df_b_av1['dYci'] = df_b_av1['dYci'] -df_b_av1.loc[0,'dYci']
    df1 = df.groupby(['new_bout_frame_number','S', 'M'])[['Heading']].mean().reset_index()
    df_b_av1['Heading'] = df1['Heading']
    df_b_av1['deltaH'] = df_b_av1['Heading'] - (df_b_av1.loc[0,'Heading'])
    df1 = df.groupby(['new_bout_frame_number'])[['Heading']].sem().reset_index()
    df_b_av1['dHci'] = df1['Heading']*1.96
    df_b_av1['dHci'] = df_b_av1['dHci'] -df_b_av1.loc[0,'dHci']
    data1 = df_b_av1[df_b_av1['S'] < 4]
    return data1


    
def TimeSeries(dfi):
    import pandas as pd
    import numpy as np 
    
    #X-Tracker Setup 
    df_xtrack_stat = dfi[dfi['State'] != 'Locomotive'].copy()
    df_xtrack_stat['Xtrack']='Stationary'
    df_xtrack_loc = dfi[dfi['State'] == 'Locomotive'].copy()
    df_xtrack_loc['Xtrack']='Locomotive'  
    dfi=pd.concat([df_xtrack_stat,df_xtrack_loc]).sort_index()
    dfi["e7"] = dfi["Xtrack"].shift(1)
    dfi["e8"] = dfi["Xtrack"] != dfi["e7"]
    dfi["e9"] = dfi["e8"].cumsum()
    dfi["e10"] = dfi.Time_ms.shift(-1)   #<-This provides the time from the row below
    
    #DAM setup
    end = round(dfi.Minutes).iloc[-1]
    a = np.arange(0,end, 1)
    b = np.arange(1,end+1, 1)
    cols = ['Time', 'BeamBreak'] #Will need to change the metric names if they change
    lst = []

    for (n, m) in zip(a, b):
        df_1min = dfi[(dfi.Minutes >= n) & (dfi.Minutes < m)]
        if len(df_1min)>1:
            x_min=df_1min["cXmm"].min()
            x_max=df_1min["cXmm"].max()
            if (int(x_min)<31.75) & (int(x_max)>32.25):
                bb = 1
            else:
                bb = 0
            lst.append([m, bb])
        else:
            lst.append([m, 1])
    df1 = pd.DataFrame(lst, columns=cols)
    
    df1["e3"] = df1["BeamBreak"].shift(1)
    df1["e4"] = df1["BeamBreak"] != df1["e3"]
    df1["Bout"] = df1["e4"].cumsum()
    df1["e6"] = df1.Time.shift(-1) 
    df1['Bout_frame_number'] = df1.groupby('Bout').cumcount()
    df2 = df1[df1['BeamBreak']==0]
    df2 = df2.groupby(['Bout']).count().reset_index()
    BoutList = df2[df2['BeamBreak'] >= 5]['Bout'].to_list()
    df_DAM = df1.query("Bout in @BoutList").copy()
    df_DAM['Hour'] = df_DAM['Time']/60
    
    
    #End Dataframe setup
    end = round(dfi.Hour).iloc[-1]
    cols = ['Hour','ZT','Fly','TruMeLan_Total', 'TruMeLan_5min', 'TruMeLan<5min', 'TruMeLan_1min',  'TruMeLan<1min',
            'XTracker_Total', 'XTracker_5min', 'XTracker<5min', 'XTracker_1min','XTracker<1min', 'DAM', 'SA', 'LO'] #Will need to change the metric names if they change
    lst = []    
    a = np.arange(0,end, 0.5)
    b = np.arange(0.5,end+0.5, 0.5)
    fly=dfi.loc[0,'Fly']
    
    for (n, m) in zip(a, b):
        df2 = dfi[(dfi.Hour<= m) & (dfi.Hour> n)]
        zt=round(df2['ZT'].iloc[-1],1)
        df2_gbmax = df2.groupby(['Bout', 'State'])[['e6']].max() 
        df2_gbmin = df2.groupby(['Bout', 'State'])[['Time_ms']].min()
        df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
        df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
        df3 = df2_gbmax - df2_gbmin
        df3=df3.reset_index()
        df3_ss = df3[df3['State'] == 'Stationary Static']
        c = df3_ss['Time'].sum() / 60000
        d = df3_ss[df3_ss['Time'] >= 300000]['Time'].sum() / 60000
        e = df3_ss[df3_ss['Time'] < 300000]['Time'].sum() / 60000 
        f = df3_ss[df3_ss['Time'] >= 60000]['Time'].sum() / 60000
        g = df3_ss[df3_ss['Time'] < 60000]['Time'].sum() / 60000
        sa = df3[df3['State'] == 'Stationary Active']['Time'].sum() / 60000
        lo = df3[df3['State'] == 'Locomotive']['Time'].sum() / 60000
            
        df2_gbmax = df2.groupby(['e9', 'Xtrack'])[['e10']].max() 
        df2_gbmin = df2.groupby(['e9', 'Xtrack'])[['Time_ms']].min()
        df2_gbmax.rename(columns={'e10':'Time'}, inplace=True)
        df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
        df3 = df2_gbmax - df2_gbmin
        df3=df3.reset_index()
        df3_xt = df3[df3['Xtrack']=='Stationary']
        h = df3_xt['Time'].sum() / 60000
        i = df3_xt[df3_xt['Time'] >= 300000]['Time'].sum() / 60000   
        j = df3_xt[df3_xt['Time'] < 300000]['Time'].sum() / 60000  
        k = df3_xt[df3_xt['Time'] >= 60000]['Time'].sum() / 60000   
        l = df3_xt[df3_xt['Time'] < 60000]['Time'].sum() / 60000  

        df_30min = df_DAM[(df_DAM.Hour > n) & (df_DAM.Hour <= m)]
        dam=len(df_30min)
        
        lst.append([m,zt,fly, c,d,e,f,g,h,i,j,k,l,dam,sa,lo])
    
    df1_df = pd.DataFrame(lst, columns=cols).clip(upper=pd.Series({'Hour': 100, 'ZT': 24,'Fly': 100,'TruMeLan_Total': 30, 'TruMeLan_5min': 30, 'TruMeLan<5min': 30, 'TruMeLan_1min': 30,  
                                                                   'TruMeLan<1min': 30, 'XTracker_Total': 30, 'XTracker_5min': 30, 'XTracker<5min': 30, 'XTracker_1min': 30,
                                                                   'XTracker<1min': 30, 'DAM': 30, 'SA': 30, 'LO': 30}), axis=1)    
    return df1_df


def TimeSeries_Setup(file):
    import os
    import os.path
    import pandas as pd
    dfs=[]
    for dirpath, dirnames, filenames in os.walk(file):
        for filename in [f for f in filenames if f=="Timeseries.csv"]:
            df=pd.read_csv(os.path.join(dirpath, filename))
            dfs.append(df)
    df=pd.concat(dfs)
    df_mean=df.groupby(['ZT']).mean().reset_index()  
    df_mean = pd.concat([df_mean[df_mean['ZT']==24], df_mean]).reset_index(drop=True)
    df_mean.loc[0,'ZT'] =0
    df_sem=df.groupby(['ZT']).sem()*1.96
    df_sem=df_sem.reset_index()
    df_sem = pd.concat([df_sem[df_sem['ZT']==24], df_sem]).reset_index(drop=True)
    df_sem.loc[0,'ZT'] =0
    return df_mean, df_sem



def Ypos_Stationary(dfi, n, day):
    import pandas as pd
    cols = ['Fly','Time of Day','Total Stationary Time', 'Total Bottom Time', 'Total Middle Time', 'Total Ceiling Time', 'Total Bottom Percentage', 
            'Total Middle Percentage', 'Total Ceiling Percentage', 'Long Bottom Bout Count', 'Long Middle Bout Count', 'Long Ceiling Bout Count',
            'Long Bottom Bout Duration', 'Long Middle Bout Duration', 'Long Ceiling Bout Duration', 'Long Bottom Total Duration', 'Long Middle Total Duration', 'Long Ceiling Total Duration',
            'Short Bottom Bout Count', 'Short Middle Bout Count', 'Short Ceiling Bout Count',
            'Short Bottom Bout Duration', 'Short Middle Bout Duration', 'Short Ceiling Bout Duration', 'Short Bottom Total Duration', 'Short Middle Total Duration', 'Short Ceiling Total Duration',
           'SA Bottom Bout Count', 'SA Middle Bout Count', 'SA Ceiling Bout Count',
            'SA Bottom Bout Duration', 'SA Middle Bout Duration', 'SA Ceiling Bout Duration', 'SA Bottom Total Duration', 'SA Middle Total Duration', 'SA Ceiling Total Duration',]
            
    lst = []
    
    if day=='Day':
        TOD='Day'
    elif day=='Night':
        TOD='Night'
    else:
        raise ValueError('Type either "Day" or "Night"')
    #Total 
    df=dfi[dfi['State'] != 'Locomotive']
    total=(len(df)/45)
    dfi_bot =df[df['cYmm'] >=2.4]
    dfi_mid =df[(df['cYmm']<2.4) &(df['cYmm']>1.5)]
    dfi_top =df[df['cYmm'] <=1.5]
    bottom_percentage = ((len(dfi_bot)/45)/total)*100
    middle_percentage = ((len(dfi_mid)/45)/total)*100
    ceiling_percentage = ((len(dfi_top)/45)/total)*100
    
    
    df2_gbmax = dfi.groupby(['Bout', 'State', 'Fly'])[['e6']].max()
    df2_gbmin = dfi.groupby(['Bout', 'State', 'Fly'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3['Seconds'] = df3['Time']/1000
    df3['sY'] = dfi.groupby(['Bout', 'State'])[['cYmm']].nth(0)
    df3['eY'] = dfi.groupby(['Bout', 'State'])[['cYmm']].nth(-1)
    df3['X'] = dfi.groupby(['Bout', 'State'])[['cXmm']].nth(0)
    df_all=df3.reset_index()
    
    df = df_all[df_all['State'].isin(['Stationary Static'])].copy()
    #Just Long SS bouts
    df_long = df[(df['Seconds'] >= 60) & (df['Seconds'] < 600000000000000000)].copy()
    df_long['Y_av'] = ((df_long['sY'] +df_long['eY'])/2) 
    long_bot =df_long[df_long['Y_av'] >=2.4]
    long_mid =df_long[(df_long['Y_av']<2.4) &(df_long['Y_av']>1.5)]
    long_top =df_long[df_long['Y_av'] <=1.5]    
    #Just Short SS bouts
    df_short = df[(df['Seconds'] >= 0.5) & (df['Seconds'] < 3)].copy()
    df_short['Y_av'] = ((df_short['sY'] +df_short['eY'])/2) 
    short_bot =df_short[df_short['Y_av'] >=2.4]
    short_mid =df_short[(df_short['Y_av']<2.4) &(df_short['Y_av']>1.5)]
    short_top =df_short[df_short['Y_av'] <=1.5]      
    
    #Just SA bouts
    df = df_all[df_all['State'].isin(['Stationary Active'])].copy()
    df_sa = df[(df['Seconds'] >= 0.5) & (df['Seconds'] < 10000000000)].copy()
    df_sa['Y_av'] = ((df_sa['sY'] +df_sa['eY'])/2) 
    sa_bot =df_sa[df_sa['Y_av'] >=2.4]
    sa_mid =df_sa[(df_sa['Y_av']<2.4) &(df_sa['Y_av']>1.5)]
    sa_top =df_sa[df_sa['Y_av'] <=1.5]      
        
    lst.append([n, TOD, total, len(dfi_bot)/45, len(dfi_mid)/45, len(dfi_top)/45,bottom_percentage,middle_percentage,ceiling_percentage, len(long_bot),len(long_mid),len(long_top),
               long_bot.Seconds.mean(),long_mid.Seconds.mean(),long_top.Seconds.mean(),long_bot.Seconds.sum(),long_mid.Seconds.sum(),long_top.Seconds.sum(),
               len(short_bot),len(short_mid),len(short_top),short_bot.Seconds.mean(),short_mid.Seconds.mean(),short_top.Seconds.mean(),short_bot.Seconds.sum(),short_mid.Seconds.sum(),short_top.Seconds.sum(), 
               len(sa_bot),len(sa_mid),len(sa_top),sa_bot.Seconds.mean(),sa_mid.Seconds.mean(),sa_top.Seconds.mean(),sa_bot.Seconds.sum(),sa_mid.Seconds.sum(),sa_top.Seconds.sum()])
    df1 = pd.DataFrame(lst, columns=cols)
    return df1
    

def Xpos_Stationary(dfi, n, day):
    import pandas as pd
    cols = ['Fly','Time of Day','Total Stationary Time', 'Total Food Time', 'Total Food Near Time', 'Total Middle Left Time', 'Total Middle Right Time', 'Total End Near Time', 'Total End Time', 
           'Total Food Percentage', 'Total Food Near Percentage', 'Total Middle Left Percentage', 'Total Middle Right Percentage', 'Total End Near Percentage', 'Total End Percentage',
           'Long Food Bout Count', 'Long Food Near Bout Count', 'Long Middle Left Bout Count', 'Long Middle Right Bout Count', 'Long End Near Bout Count', 'Long End Bout Count',
          'Long Food Bout Duration', 'Long Food Near Bout Duration', 'Long Middle Left Bout Duration', 'Long Middle Right Bout Duration', 'Long End Near Bout Duration', 'Long End Bout Duration',
            'Long Food Total Duration', 'Long Food Near Total Duration', 'Long Middle Left Total Duration', 'Long Middle Right Total Duration', 'Long End Near Total Duration', 'Long End Total Duration',
            'Short Food Bout Count', 'Short Food Near Bout Count', 'Short Middle Left Bout Count', 'Short Middle Right Bout Count', 'Short End Near Bout Count', 'Short End Bout Count',
          'Short Food Bout Duration', 'Short Food Near Bout Duration', 'Short Middle Left Bout Duration', 'Short Middle Right Bout Duration', 'Short End Near Bout Duration', 'Short End Bout Duration',
            'Short Food Total Duration', 'Short Food Near Total Duration', 'Short Middle Left Total Duration', 'Short Middle Right Total Duration', 'Short End Near Total Duration', 'Short End Total Duration',
             'SA Food Bout Count', 'SA Food Near Bout Count', 'SA Middle Left Bout Count', 'SA Middle Right Bout Count', 'SA End Near Bout Count', 'SA End Bout Count',
          'SA Food Bout Duration', 'SA Food Near Bout Duration', 'SA Middle Left Bout Duration', 'SA Middle Right Bout Duration', 'SA End Near Bout Duration', 'SA End Bout Duration',
            'SA Food Total Duration', 'SA Food Near Total Duration', 'SA Middle Left Total Duration', 'SA Middle Right Total Duration', 'SA End Near Total Duration', 'SA End Total Duration']
            
    lst = []
    
    if day=='Day':
        TOD='Day'
    elif day=='Night':
        TOD='Night'
    else:
        raise ValueError('Type either "Day" or "Night"')
    #Total 
    df=dfi[dfi['State'] != 'Locomotive']
    total=(len(df)/45)
    
    dfi_food =df[(df['cXmm']<14) &(df['cXmm']>=4)]
    dfi_foodnear =df[(df['cXmm']<24) &(df['cXmm']>=14)]
    dfi_middleleft =df[(df['cXmm']<34) &(df['cXmm']>=24)]
    dfi_middleright =df[(df['cXmm']<44) &(df['cXmm']>=34)]
    dfi_endnear =df[(df['cXmm']<54) &(df['cXmm']>=44)]
    dfi_end =df[(df['cXmm']<64) &(df['cXmm']>=54)]
    
    
    df2_gbmax = dfi.groupby(['Bout', 'State', 'Fly'])[['e6']].max()
    df2_gbmin = dfi.groupby(['Bout', 'State', 'Fly'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3['Seconds'] = df3['Time']/1000
    df3['sY'] = dfi.groupby(['Bout', 'State'])[['cYmm']].nth(0)
    df3['eY'] = dfi.groupby(['Bout', 'State'])[['cYmm']].nth(-1)
    df3['X'] = dfi.groupby(['Bout', 'State'])[['cXmm']].nth(0)
    df_all=df3.reset_index()
    
    #Just Long SS bouts
    df = df_all[df_all['State'].isin(['Stationary Static'])].copy()
    df_long = df[(df['Seconds'] >= 60) & (df['Seconds'] < 600000000000000000)].copy()
    df_long['Y_av'] = ((df_long['sY'] +df_long['eY'])/2)
    
    long_food =df_long[(df_long['X']<14) &(df_long['X']>=4)]
    long_foodnear =df_long[(df_long['X']<24) &(df_long['X']>=14)]
    long_middleleft =df_long[(df_long['X']<34) &(df_long['X']>=24)]
    long_middleright =df_long[(df_long['X']<44) &(df_long['X']>=34)]
    long_endnear =df_long[(df_long['X']<54) &(df_long['X']>=44)]
    long_end =df_long[(df_long['X']<64) &(df_long['X']>=54)]    
    
    
    #Just Short SS bouts
    df = df_all[df_all['State'].isin(['Stationary Static'])].copy()
    df_short = df[(df['Seconds'] >= 0.5) & (df['Seconds'] < 60)].copy()
    df_short['Y_av'] = ((df_short['sY'] +df_short['eY'])/2) 
    
    short_food =df_short[(df_short['X']<14) &(df_short['X']>=4)]
    short_foodnear =df_short[(df_short['X']<24) &(df_short['X']>=14)]
    short_middleleft =df_short[(df_short['X']<34) &(df_short['X']>=24)]
    short_middleright =df_short[(df_short['X']<44) &(df_short['X']>=34)]
    short_endnear =df_short[(df_short['X']<54) &(df_short['X']>=44)]
    short_end =df_short[(df_short['X']<64) &(df_short['X']>=54)]        
    
    #Just SA bouts
    df = df_all[df_all['State'].isin(['Stationary Active'])].copy()
    df_sa = df[(df['Seconds'] >= 0.5) & (df['Seconds'] < 10000000000)].copy()
    df_sa['Y_av'] = ((df_sa['sY'] +df_sa['eY'])/2) 
    
    sa_food =df_sa[(df_sa['X']<14) &(df_sa['X']>=4)]
    sa_foodnear =df_sa[(df_sa['X']<24) &(df_sa['X']>=14)]
    sa_middleleft =df_sa[(df_sa['X']<34) &(df_sa['X']>=24)]
    sa_middleright =df_sa[(df_sa['X']<44) &(df_sa['X']>=34)]
    sa_endnear =df_sa[(df_sa['X']<54) &(df_sa['X']>=44)]
    sa_end =df_sa[(df_sa['X']<64) &(df_sa['X']>=54)]      
        
    lst.append([n, TOD, total, len(dfi_food)/45, len(dfi_foodnear)/45, len(dfi_middleleft)/45,len(dfi_middleright)/45,len(dfi_endnear)/45,len(dfi_end)/45,
                ((len(dfi_food)/45)/total)*100,((len(dfi_foodnear)/45)/total)*100,((len(dfi_middleleft)/45)/total)*100,((len(dfi_middleright)/45)/total)*100,((len(dfi_endnear)/45)/total)*100,((len(dfi_end)/45)/total)*100,
                len(long_food),len(long_foodnear),len(long_middleleft),len(long_middleright),len(long_endnear),len(long_end),
                long_food.Seconds.mean(),long_foodnear.Seconds.mean(),long_middleleft.Seconds.mean(),long_middleright.Seconds.mean(),long_endnear.Seconds.mean(),long_end.Seconds.mean(),
                long_food.Seconds.sum(),long_foodnear.Seconds.sum(),long_middleleft.Seconds.sum(),long_middleright.Seconds.sum(),long_endnear.Seconds.sum(),long_end.Seconds.sum(),
                len(short_food),len(short_foodnear),len(short_middleleft),len(short_middleright),len(short_endnear),len(short_end),
                short_food.Seconds.mean(),short_foodnear.Seconds.mean(),short_middleleft.Seconds.mean(),short_middleright.Seconds.mean(),short_endnear.Seconds.mean(),short_end.Seconds.mean(),
                short_food.Seconds.sum(),short_foodnear.Seconds.sum(),short_middleleft.Seconds.sum(),short_middleright.Seconds.sum(),short_endnear.Seconds.sum(),short_end.Seconds.sum(),
                len(sa_food),len(sa_foodnear),len(sa_middleleft),len(sa_middleright),len(sa_endnear),len(sa_end),
                sa_food.Seconds.mean(),sa_foodnear.Seconds.mean(),sa_middleleft.Seconds.mean(),sa_middleright.Seconds.mean(),sa_endnear.Seconds.mean(),sa_end.Seconds.mean(),
                sa_food.Seconds.sum(),sa_foodnear.Seconds.sum(),sa_middleleft.Seconds.sum(),sa_middleright.Seconds.sum(),sa_endnear.Seconds.sum(),sa_end.Seconds.sum(),])
                
    df1 = pd.DataFrame(lst, columns=cols)
    return df1


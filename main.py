from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from UCS import generateDirectedGraph,UCS_code
import networkx as nx
import matplotlib.pyplot as plt
import json


def start():
    weighted_edges.append([input1.get(),input2.get(),float(input3.get())])
    G.add_edge(input1.get(),input2.get(),km=float(input3.get()))
    lsb.insert(END,input1.get()+' đến '+input2.get()+' : '+ str(float(input3.get()))+' km')
    label1_input.delete(0,END)
    label2_input.delete(0,END)
    label3_input.delete(0,END)
    draw_edge(check_edge())


def delete(event):
    #lay vi tri cac diem
    pos=check_edge()
    possition_list=lsb.curselection()
    lsb.delete(int(possition_list[0]))
    G.remove_edge(weighted_edges[int(possition_list[0])][0],weighted_edges[int(possition_list[0])][1])
    list_position=weighted_edges[int(possition_list[0])]
    for edges in weighted_edges:
        if edges[0]==list_position[0] and edges[1]==list_position[1] and edges[2]==list_position[2] or edges[0]==list_position[1] and edges[1]==list_position[0] and edges[2]==list_position[2]: 
             weighted_edges.remove(edges)
    G_nodes=G.nodes#lay cac nut
    G.clear()
    for edge in weighted_edges:
        G.add_edge(edge[0],edge[1],km=edge[2])
    for j in G_nodes:
        fixed_positions[j]=list(pos[j])#dict 'nut' : vitri
    draw_edge(check_edge())
    lsb_ucs.delete(0)
    length1_ucs.delete(0)


def UCS_AI():
    plt.clf()
    lsb_ucs.delete(0)
    length1_ucs.delete(0)
    directed_weighted_graph=generateDirectedGraph(weighted_edges)
    Bool_ip1 = False
    Bool_ip2 = False
    for i in weighted_edges:
        if input1_dj.get() in i:
            Bool_ip1 = True
        if input2_dj.get() in i:
            Bool_ip2 = True
    if Bool_ip1 ==True and Bool_ip2 == True:
        ucs =UCS_code(directed_weighted_graph,input1_dj.get(), input2_dj.get())
        try:
            lsb_ucs.insert(0, ucs[0])
            length1_ucs.insert(0,ucs[1])
            s1=ucs[0].split('-')
            list_dj=[]
            if input1_dj.get()!=input2_dj.get():
                for i in range(len(s1)):
                    try:
                        list_dj.append([s1[i],s1[i+1]])
                        list_dj.append([s1[i+1],s1[i]])
                    except:
                        pass
                list_elarge=[]
                for i in list_dj:
                    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if u==i[0] and v==i[1]]
                    try:
                        list_elarge.append(elarge[0])
                    except:
                        pass
                draw_edge(check_edge(),list_elarge)
        except:
            showerror('Lỗi', 'Không tìm thấy đường đi!')
            
    else:
        showerror('Lỗi','Không tìm thấy đường đi!')
        draw_edge(check_edge())


def request():
    plt.clf()
    G.clear()
    weighted_edges.clear()
    lsb_ucs.delete(0)
    length1_ucs.delete(0)
    lsb.delete(0,END)
    label1_input.delete(0,END)
    label2_input.delete(0,END)
    label3_input.delete(0,END)
    label1_ucs_input.delete(0,END)
    label2_ucs_input.delete(0,END)
    Combo['values'] =''
    Combo.set('Điểm')
    lsb_nodes.delete(0,END)
    fixed_positions.clear()
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.show(block=False)


def change_position_node(item):
    pos=check_edge()
    G_nodes=G.nodes#lay cac nut
    G.clear()
    for edge in weighted_edges:
        G.add_edge(edge[0],edge[1],km=edge[2])
    for j in G_nodes:
        fixed_positions[j]=list(pos[j])#dict 'nut' : vitri
    if item == '+x':
        fixed_positions[get_node][0]=fixed_positions[get_node][0]+float(get_score) 
    elif item =='-x':
        fixed_positions[get_node][0]=fixed_positions[get_node][0]-float(get_score) 
    elif item =='+y':
        fixed_positions[get_node][1]=fixed_positions[get_node][1]+float(get_score) 
    elif item =='-y':
        fixed_positions[get_node][1]=fixed_positions[get_node][1]-float(get_score) 
    draw_edge(check_edge())


def get_combo(event):
    global get_node,get_score
    get_node=selected_node.get()
    get_score=selected_score.get()

def check_edge():
    if not fixed_positions:
        pos = nx.spring_layout(G ,seed=7)
    else:
        fixed_nodes = fixed_positions.keys()
        pos = nx.spring_layout(G,pos=fixed_positions, fixed = fixed_nodes,seed=7)
    return pos 

def draw_edge(pos,list_elarge=None):
    lsb_nodes.delete(0,END)
    if list_elarge==None:
        plt.clf()
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos,width=1)
    if list_elarge:
        nx.draw_networkx_edges(
        G, pos, edgelist=list_elarge, width=4, edge_color="r"
        )
    edge_labs = dict([( (u,v), d['km']) for u,v,d in G.edges(data=True)])
    nx.draw(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labs)
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    G_nodes=G.nodes
    Combo['values'] = [m for m in G_nodes] #cac gia tri trong combobox
    for j in G_nodes:
        lsb_nodes.insert(END,j)
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.show(block=False)


def save_file():
    if len(file_input.get())>=1:
        list_file.delete(0,END)
        data={}
        with open('data.json') as file:
            data=json.loads(file.read())
            data[file_input.get()]=[]
            data[file_input.get()].append({
                'edges':weighted_edges,
                'node_position':fixed_positions
            })
        with open('data.json', 'w') as file:
            json.dump(data, file)
            keylist = data.keys()
        for i in keylist:
            list_file.insert(END,i)
        file_input_text.delete(0,END)
        showinfo('Thông báo!','Lưu file thành công')
    else:
        pass


def get_file(event):
    request()
    select =list_file.curselection()
    with open('data.json') as json_file:
        data = json.load(json_file)
        key=list_file.get(select[0])
        node_position=data[list_file.get(select[0])][0]['node_position']
        for edge in data[key]: 
            for i in edge['edges']:
                input1.set(i[0])
                input2.set(i[1])
                input3.set(i[2])
                start()
        for j in node_position:
            fixed_positions[j]=list(node_position[j])#dict 'nut' : vitri
        draw_edge(check_edge())


def delete_file(event):
    select =list_file.curselection()
    with open('data.json') as json_file:
        data = json.load(json_file)
    data.pop(list_file.get(select[0]))
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file)
        keylist = data.keys()
    list_file.delete(0,END)
    for i in keylist:
        list_file.insert(END,i)
 



#---------------------------------Tkinter------------------------------------------------------------------------
window = Tk()
window.title('Tìm đường đi ngắn nhất')
window.geometry("500x600+900+100")
plt.rcParams["figure.figsize"] = (8,6)
#---------------------
weighted_edges=[]    #
fixed_positions={}   #
get_node=''          #
get_score=''         #
#---------------------
G=nx.Graph()
input1=StringVar()
input2=StringVar()
input3=StringVar()

label1=Label(window,text='Điểm bắt đầu')
label1.place(x=200,y=10)
label1_input=Entry(window,textvariable=input1)
label1_input.place(x=180,y=30)

label2=Label(window,text='Điểm kết thúc')
label2.place(x=200,y=50)
label2_input=Entry(window,textvariable=input2)
label2_input.place(x=180,y=70)

label3=Label(window,text='Độ dài')
label3.place(x=200,y=90)
label3_input=Entry(window,textvariable=input3)
label3_input.place(x=180,y=110)
label3_km=Label(window,text='km')
label3_km.place(x=300,y=110)

plot_button = Button(master = window, 
                     command = start,
                     height = 2, 
                     width = 10,
                     text = "Hiển thị")
plot_button.place(x=200,y=130)

label_lsb=Label(window,text='Dữ liệu')
label_lsb.place(x=220,y=180)
lsb=Listbox(window)
lsb.place(x=180,y=200)

label_lsb_nodes=Label(window,text='Điểm')
label_lsb_nodes.place(x=140,y=180)
lsb_nodes=Listbox(window,width=5)
lsb_nodes.place(x=140,y=200)

file_input=StringVar()
file_name=Label(window,text='Tên')
file_name.place(x=340,y=180)
file_input_text=Entry(window,textvariable=file_input,width = 10)
file_input_text.place(x=370,y=180)
file_save = Button(master = window, 
                     command = save_file,
                     height = 1, 
                     width = 6,
                     text = "Lưu data")
file_save.place(x=440,y=175)
list_file_json=Label(window,text='Danh sách data')
list_file_json.place(x=360,y=210)
list_file=Listbox(window,width=17,height = 8)
list_file.place(x=350,y=230)
with open('data.json') as file:
    data=json.loads(file.read())
    keylist = data.keys()
    for i in keylist:
        list_file.insert(END,i)
delete_file_btn=Button(window,text='Xóa data')
delete_file_btn.place(x=350,y=370)
delete_file_btn.bind('<Button-1>',delete_file)


launch_file=Button(window,text='xuất data')
launch_file.place(x=410,y=370)
launch_file.bind('<Button-1>',get_file)

#=========change_position=======
change_position=Label(window,text='Thay đổi vị trí')
change_position.place(x=30,y=180)

selected_node = StringVar()
Combo = ttk.Combobox(window, textvariable=selected_node,width=5,height=5)
Combo['state'] = 'readonly'
Combo.set('Điểm')
Combo.place(x=50,y=220)
Combo.bind('<<ComboboxSelected>>', get_combo)

selected_score=StringVar()
Combo_score = ttk.Combobox(window, textvariable=selected_score,width=5,height=1)
Combo_score['values'] = [0.001,0.01,0.1]
Combo_score['state'] = 'readonly'
Combo_score.set('Chọn')
Combo_score.place(x=50,y=270)
Combo_score.bind('<<ComboboxSelected>>', get_combo)

bt_increse_x=Button(window,text='>',height=1,command= lambda: change_position_node('+x'))
bt_increse_x.place(x=85,y=265)
bt_decrease_x=Button(window,text='<',height=1,command= lambda: change_position_node('-x'))
bt_decrease_x.place(x=33,y=265)
bt_increse_y=Button(window,text='^',width=4,command= lambda: change_position_node('+y'))
bt_increse_y.place(x=50,y=245)
bt_decrease_y=Button(window,text='v',width=4,command= lambda: change_position_node('-y'))
bt_decrease_y.place(x=50,y=295)
#=======end change=====
bt_delete=Button(window,text='Xóa')
bt_delete.place(x=220,y=370)
bt_delete.bind('<Button-1>',delete)
#------------------UCS----------------------------------
input1_dj=StringVar()
input2_dj=StringVar()

label_ucs=Label(window,text='Tìm Đường đi ngắn nhất')
label_ucs.place(x=170,y=430)

label1_ucs=Label(window,text='Từ')
label1_ucs.place(x=100,y=460)
label1_ucs_input=Entry(window,textvariable=input1_dj,width=10)
label1_ucs_input.place(x=120,y=460)

label2_ucs=Label(window,text='Đến')
label2_ucs.place(x=190,y=460)
label2_ucs_input=Entry(window,textvariable=input2_dj,width=10)
label2_ucs_input.place(x=220,y=460)

road_ucs=Button(window,text='Tìm',width=7,command=UCS_AI)
road_ucs.place(x=290,y=458)

label3_ucs=Label(window,text='Đường')
label3_ucs.place(x=100,y=490)

lsb_ucs=Listbox(window,height=1)
lsb_ucs.place(x=140,y=490)

length_ucs=Label(window,text='Dài')
length_ucs.place(x=265,y=490)
length1_ucs=Listbox(window,height=1,width=10)
length1_ucs.place(x=290,y=490)
#------------------end UCS----------------------------------
btn_request = Button(master = window,  
                    command=request,                
                     height = 2, 
                     width = 10,
                     text = "Làm mới")
btn_request.place(x=200,y=510)


window.mainloop()

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from UCS import generateDirectedGraph,UCS_code
import networkx as nx
import matplotlib.pyplot as plt
from sample import node_position,edges


def start():
    global i
    fixed_positions.clear()
    weighted_edges.append([input1.get(),input2.get(),float(input3.get())])
    G.add_edge(input1.get(),input2.get(),km=float(input3.get()))
    lsb.insert(END,weighted_edges[i][0]+' đến '+weighted_edges[i][1]+' là '+ str(weighted_edges[i][2])+' km')
    i+=1
    label1_input.delete(0,END)
    label2_input.delete(0,END)
    label3_input.delete(0,END)
    pos = nx.spring_layout(G ,seed=7)
    draw_edge(pos)


def delete(event):
    global i
    #lay vi tri cac diem
    # fixed_positions.clear()
    pos=check_edge()
    possition_list=lsb.curselection()
    lsb.delete(int(possition_list[0]))
    G.remove_edge(weighted_edges[int(possition_list[0])][0],weighted_edges[int(possition_list[0])][1])
    list_position=weighted_edges[int(possition_list[0])]
    for edges in weighted_edges:
        if edges[0]==list_position[0] and edges[1]==list_position[1] and edges[2]==list_position[2] or edges[0]==list_position[1] and edges[1]==list_position[0] and edges[2]==list_position[2]: 
             weighted_edges.remove(edges)
    i-=1

    G_nodes=G.nodes#lay cac nut
    G.clear()
    for edge in weighted_edges:
        G.add_edge(edge[0],edge[1],km=edge[2])
    for j in G_nodes:
        fixed_positions[j]=list(pos[j])#dict 'nut' : vitri
    fixed_nodes = fixed_positions.keys()
    pos = nx.spring_layout(G,pos=fixed_positions, fixed = fixed_nodes,seed=7)
    draw_edge(pos)
    lsb_dijkstra.delete(0)
    length1_dijkstra.delete(0)

def UCS_AI():
    plt.clf()
    lsb_dijkstra.delete(0)
    length1_dijkstra.delete(0)
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
        lsb_dijkstra.insert(0,ucs[0])
        length1_dijkstra.insert(0,ucs[1])
        s1=ucs[0].split('-')
        list_dj=[]
        if input1_dj.get()!=input2_dj.get():
            for i in range(len(s1)):
                try:
                    list_dj.append([s1[i],s1[i+1]])
                    list_dj.append([s1[i+1],s1[i]])
                except:
                    pass
            for i in list_dj:
                elarge = [(u, v) for (u, v, d) in G.edges(data=True) if u==i[0] and v==i[1]]
                draw_edge(check_edge(),elarge)
            
    else:
        showinfo('Lỗi','Không tìm thấy đường đi!')
        draw_edge(check_edge())


def request():
    global i
    plt.clf()
    G.clear()
    weighted_edges.clear()
    i=0
    lsb_dijkstra.delete(0)
    length1_dijkstra.delete(0)
    lsb.delete(0,END)
    label1_input.delete(0,END)
    label2_input.delete(0,END)
    label3_input.delete(0,END)
    label1_dijkstra_input.delete(0,END)
    label2_dijkstra_input.delete(0,END)
    Combo['values'] =''
    Combo.set('')
    lsb_nodes.delete(0,END)
    plt.show(block=False)

def draw_edge(pos,elarge=None):
    lsb_nodes.delete(0,END)
    if elarge==None:
        plt.clf()
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos,width=1)
    if elarge:
        nx.draw_networkx_edges(
        G, pos, edgelist=elarge, width=4, edge_color="r"
        )
    edge_labs = dict([( (u,v), d['km']) for u,v,d in G.edges(data=True)])
    nx.draw(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labs)
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    G_nodes=G.nodes
    Combo['values'] = [m for m in G_nodes] #cac gia tri trong combobox
    for j in G_nodes:
        lsb_nodes.insert(END,j)
    plt.show(block=False)

def check_edge():
    if not fixed_positions:
        pos = nx.spring_layout(G ,seed=7)
    else:
        fixed_nodes = fixed_positions.keys()
        pos = nx.spring_layout(G,pos=fixed_positions, fixed = fixed_nodes,seed=7)
    return pos 

def get_combo(event):
    global get_node,get_score
    get_node=''
    get_score=''
    get_node=selected_node.get()
    get_score=selected_score.get()



def change_position_node(item):
    pos=check_edge()
    G_nodes=G.nodes#lay cac nut
    G.clear()
    for edge in weighted_edges:
        G.add_edge(edge[0],edge[1],km=edge[2])
    for j in G_nodes:
        fixed_positions[j]=list(pos[j])#dict 'nut' : vitri
    fixed_nodes = fixed_positions.keys()
    if item == '+x':
        fixed_positions[get_node][0]=fixed_positions[get_node][0]+float(get_score) 
    elif item =='-x':
        fixed_positions[get_node][0]=fixed_positions[get_node][0]-float(get_score) 
    elif item =='+y':
        fixed_positions[get_node][1]=fixed_positions[get_node][1]+float(get_score) 
    elif item =='-y':
        fixed_positions[get_node][1]=fixed_positions[get_node][1]-float(get_score) 
    pos = nx.spring_layout(G,pos=fixed_positions, fixed = fixed_nodes,seed=7)
    draw_edge(pos)


def sample():
    for edge in edges:
        input1.set(edge[0])
        input2.set(edge[1])
        input3.set(edge[2])
        start()
    for j in node_position:
        fixed_positions[j]=list(node_position[j])#dict 'nut' : vitri
    fixed_nodes = fixed_positions.keys()
    pos = nx.spring_layout(G,pos=fixed_positions, fixed = fixed_nodes,seed=7)
    draw_edge(pos)


#---------------------------------Tkinter------------------------------------------------------------------------
window = Tk()
window.title('Tìm đường đi ngắn nhất')
window.geometry("500x600+900+100")
plt.rcParams["figure.figsize"] = (8,6)
#---------------------
i=0                  #
weighted_edges=[]    #
fixed_positions={}   #
list_node=[]         #
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
#----------------------------------------------------------------------------
input1_dj=StringVar()
input2_dj=StringVar()
label_dijkstra=Label(window,text='Tìm Đường đi ngắn nhất')
label_dijkstra.place(x=170,y=400)
label1_dijkstra=Label(window,text='Từ')
label1_dijkstra.place(x=100,y=430)
label1_dijkstra_input=Entry(window,textvariable=input1_dj,width=10)
label1_dijkstra_input.place(x=120,y=430)
#------------------Dijkstra----------------------------------
label2_dijkstra=Label(window,text='Đến')
label2_dijkstra.place(x=190,y=430)
label2_dijkstra_input=Entry(window,textvariable=input2_dj,width=10)
label2_dijkstra_input.place(x=220,y=430)

road_dijkstra=Button(window,text='Tìm',width=7,command=UCS_AI)
road_dijkstra.place(x=290,y=428)

label3_dijkstra=Label(window,text='Đường')
label3_dijkstra.place(x=100,y=460)
lsb_dijkstra=Listbox(window,height=1)
lsb_dijkstra.place(x=140,y=460)
length_dijkstra=Label(window,text='Dài')
length_dijkstra.place(x=265,y=460)
length1_dijkstra=Listbox(window,height=1,width=10)
length1_dijkstra.place(x=290,y=460)

btn_request = Button(master = window,  
                    command=request,                
                     height = 2, 
                     width = 10,
                     text = "Làm mới")
btn_request.place(x=200,y=480)

sample_request = Button(master = window,  
                    command=sample,                
                     height = 2, 
                     width = 10,
                     text = "ví dụ")
sample_request.place(x=200,y=540)

window.mainloop()

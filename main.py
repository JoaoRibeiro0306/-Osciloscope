
import T_Display
import gc
import time
import math

# Função de leitura dos valores do ADC e representação no display
def read_and_display(escala_tensão, escala_tempo, return_values, print): #Os argumentos return_values e print vão ser usados para definir quando é necessário dar return dos valores calculados ou quando é necessário imprimir a onda no display
    gc.collect()
    Vmax, Vmin, Vmed, Vrms = 0, 0, 0, 0
    V_squared = 0
    squared_sum = 0

    if(print):
        tft.display_set(tft.BLACK, 0, 0, 240, 135)         # Apaga display
        tft.display_write_grid(0, 0, width_max, height_max-16, divisoes_x, divisoes_y, True) # Desenha grelha (c/ linhas centrais)
        tft.set_wifi_icon(width_max-16,height_max-16)                        # Coloca o icon wifi no display
        str1 = "%dV/" % escalas_tensão[escala_tensão]                       
        str2 = "%dms/" % escalas_tempo[escala_tempo]
        tft.display_write_str(tft.Arial16, str1, 0, height_max-16)           #Apresenta a escala de tensão 
        tft.display_write_str(tft.Arial16, str2, 100, height_max-16)         #Apresenta a escala do tempo
    
    pontos_adc = tft.read_adc(240, escalas_tempo[escala_tempo] * divisoes_x)
    x=[]
    pontos_graf=[]
    pontos_volt=[]

    for n in range(width_max):
        V = 0.00044028 * pontos_adc[n] + 0.091455 # Converte valor do ADC em Volt (sem calibracao)
        #V = 0.00042899 * pontos_adc[n] + 0.10677016  # Converte valor do ADC em Volt (com calibracao)
        V = V - 1 # Tensão entrada de referência de 1V
        V = V / fator # Entra com o efeito do div. resistivo
        pontos_volt.append(V)
        pixel = round((V/(escalas_tensão[escala_tensão]/((height_max-16)/divisoes_y))) + ((height_max-16)/2)) #pontos para por no display. A primeira parcela calcula a tensão com a respetiva escala e a segunda e terceira vão centrar a onda no inicio da grid
        if pixel>height_max-16: #Se o valor da onda exceder o tamanho do display, dar print no limite do display
                pixel = height_max-16
        if pixel<0:
            pixel = 0
        if n==0: # Caso seja o primeiro ponto
            Vmax = Vmin = Vmed = V
        else:
            Vmed += V
            if V>Vmax: Vmax=V
            if V<Vmin: Vmin=V
        V_squared = V*V  
        squared_sum += V_squared #Soma do quadrado de cada ponto para calcular Vrms
        pontos_graf.append(pixel)
        x.append(n)
    gc.collect()

    Vrms = ((squared_sum/width_max)**0.5) #Raiz quadrada da média dos valores de cada ponto ao quadrado
    Vmed /= width_max # Divide pelo número de amostras
    
    if(print):
        tft.display_nline(tft.YELLOW, x, pontos_graf)   #Imprime os pontos no osciloscópio
        del x, pontos_graf
    if(return_values):
        return Vmax, Vmin, Vmed, Vrms, pontos_volt      #Quando é necessario devolver os valores das tensões
    else:
        del Vmax,Vmin,Vmed,Vrms,pontos_volt             #Quando não é necessario devolver os valores das tensões
        return
    
def send_mail():
    tft.display_set(tft.BLACK, 0, 0, 240, 135)         # Apaga display
    tft.set_wifi_icon(0,height_max-16)                 # Coloca o icon wifi no display
    str_1= "Deseja mesmo enviar o email"               
    str_4 = "para"
    str_5 = "%s?" % mail_to
    str_2= "Sim --->"
    str_3= "Nao --->"
    tft.display_write_str(tft.Arial16, str_1, 0, 67+16)     #Apresenta menu para utilizador confirmar se pretende enviar um email
    tft.display_write_str(tft.Arial16, str_4, 0, 67)
    tft.display_write_str(tft.Arial16, str_5, 0, 67-16)
    tft.display_write_str(tft.Arial16, str_2, width_max-60, height_max-16)
    tft.display_write_str(tft.Arial16, str_3, width_max-60, 0)

    del str_1, str_2, str_3, str_4, str_5       
    
    gc.collect()

    while tft.working():                              # Verifica se o utilizador pressionou "Sim" ou "Não"
        but=tft.readButton()                          # Lê estado dos botões
        if but!=tft.NOTHING:
            if but==11:                               # Button 1 click - Envia o e-mail (Sim)
                break
            if but==21:                               # Button 2 click - Volta a dar display do sinal (Não)
                read_and_display(escala_tensão, escala_tempo, 0, 1)
                return
    
    Vmax, Vmin, Vmed, Vrms, pontos_volt = read_and_display(escala_tensão, escala_tempo, 1, 0)   #Calcula os valores das tensões para serem enviadas no e-mail
    corpo_mail = "Vmax = {}\n Vmin = {}\n Vmed = {}\n Vrms = {}".format(Vmax, Vmin, Vmed, Vrms)     
    del Vmax, Vmin, Vmed, Vrms
    tft.send_mail(0.01, pontos_volt, corpo_mail,  mail_to)         #Envia o e-mail
    del pontos_volt
    return 
                
            
    
def volt_values():          #Dá display aos valores de Vmax, Vmin, Vmed e Vrms
    gc.collect()

    Vmax, Vmin, Vmed, Vrms, pontos_volt = read_and_display(escala_tensão, escala_tempo, 1, 0)       #Calcula os valores
    del pontos_volt

    tft.display_set(tft.BLACK, 0, 0, width_max, height_max)         # Apaga display
    tft.set_wifi_icon(0,135-16)                                     # Coloca o icon wifi no display
    
    str1 = "Vmax = %.2f" % Vmax
    str2 = "Vmin = %.2f" % Vmin
    str3 = "Vmed = %.2f" % Vmed
    str4 = "Vrms = %.2f" % Vrms
    tft.display_write_str(tft.Arial16, str1, 10, 20+80)             #Dá display
    tft.display_write_str(tft.Arial16, str2, 10, 20+60)
    tft.display_write_str(tft.Arial16, str3, 10, 20+40)
    tft.display_write_str(tft.Arial16, str4, 10, 20+20)

    del Vmax, Vmin, Vmed, Vrms, str1, str2, str3, str4
    
def calibrate_device():
   
    valores_teste = [10, 5, 0, -5, -10]         #Diferentes valores da tensão de entrada usados na calibração
    
    
    for k in range(len(valores_teste)): 
        V = 0
        V_sum_teste = [0.0]*100
        V_mean = [0.0]*100
        V_sample_min = 0
        tft.display_set(tft.BLACK, 0, 0, 240, 135)         # Apaga display
        tft.set_wifi_icon(0,height_max-16)                 # Coloca o icon wifi no display
        str2 = "Calibracao"
        str3 = "Introduza %dV DC" %valores_teste[k]
        str4= "Continuar --->"
        str5= "Sair --->"
        tft.display_write_str(tft.Arial16, str2, 50, height_max-64) #Apresenta menu que realiza a interface com o utilizador durante o processo de calibração
        tft.display_write_str(tft.Arial16, str3, 50, height_max-80)
        tft.display_write_str(tft.Arial16, str4, width_max-105, height_max-16)
        tft.display_write_str(tft.Arial16, str5, width_max-60, 0)
        del str2,str3,str4,str5

        while tft.working():                       
            but=tft.readButton()                          # Lê estado dos botões
            if but!=tft.NOTHING:
                if but==11:                           # Button 1 click - Continua com o procedimento (Continuar)
                    break
                if but==21: 
                    read_and_display(escala_tensão, escala_tempo, 0, 1)  #Button 2 click - Volta a apresentar o sinal de entrada (Sair)
                    return

        for n in range(100):    #Cálculo da média de valores do ADC para 100 amostras de 100 pontos
            pontos_adc = tft.read_adc(100, 100)
            for j in range(100):
                V = pontos_adc[j]
                V_sum_teste[j] += V 
                
        for i in range(100):
            V_mean[i] = V_sum_teste[i]/100 
            V_sample_min += V_mean[i]
        
        V_sample_min /= 100
        
        str1 = "Vmean = %f" % V_sample_min 
        str2 = "Continuar?"
        str4= "Continuar --->"
        str5= "Sair --->"
        tft.display_set(tft.BLACK, 0, 0, 240, 135)         # Apaga display
        tft.set_wifi_icon(0,height_max-16)                        # Coloca o icon wifi no display
        tft.display_write_str(tft.Arial16, str1, 50, height_max-64)    #Apresenta o valor digital médio recolhido
        tft.display_write_str(tft.Arial16, str2, 50, height_max-80)
        tft.display_write_str(tft.Arial16, str4, width_max-105, height_max-16)
        tft.display_write_str(tft.Arial16, str5, width_max-60, 0)
        del str1, str2, str4, str5

        while tft.working():                        
            but=tft.readButton()                          # Lê estado dos botões
            if but!=tft.NOTHING:
                if but==11:                           # Button 1 click - Repete função (Continuar)
                    break
                if but==21: 
                    read_and_display(escala_tensão, escala_tempo, 0, 1)  #Button 2 click - Volta a apresentar o sinal de entrada (Sair)
                    return
    
def calc_DFT(escala_tempo, escala_tensão, printf):
    gc.collect
    pontos_volt=[]
    
    pontos_volt = tft.read_adc(width_max, escalas_tempo[escala_tempo] * divisoes_x)
    
    for n in range(width_max):
        V = 0.00044028 * pontos_volt[n] + 0.091455
        #V = 0.00042899 * pontos_volt[n] + 0.10677016  # Converte valor do ADC em Volt (com calibracao)
        V = V - 1 # Tensão entrada de referência de 1V
        V = V / fator # Entra com o efeito do div. resistivo
        pontos_volt[n] = V
        
    gc.collect()  

    Xk = calc_Xk(pontos_volt)   #Calcula o módulo da Transformada de Fourier

    del pontos_volt, V
    
    spect_Xk = [0]*width_max
    
    for freq in range(width_max):       #Calcula o espetro da Transformada de Fourier, tendo em conta que cada ponto em frequência corresponde a dois pixeis
        if freq == 0 or freq == 1 or freq == (width_max-1) or freq == width_max:
            spect_Xk[freq] = round(Xk[freq]/width_max)
            if(spect_Xk[freq] > height_max-16): #Se um ponto excede a altura máxima permitida então é representado como se estivesse na altura máxima
                spect_Xk[freq] = height_max-16
                
        else:
            spect_Xk[freq] = round(2*(Xk[freq]/width_max))
            if(spect_Xk[freq] > height_max-16): #Se um ponto excede a altura máxima permitida então é representado como se estivesse na altura máxima
                spect_Xk[freq] = height_max-16
    del Xk
            
    freq=[n for n in range(0,width_max,1)]
    
    if(printf):
        tft.display_set(tft.BLACK, 0, 0, 240, 135)         # Apaga display
        tft.display_write_grid(0, 0, width_max, height_max-16, divisoes_x, divisoes_y, False) # Desenha grelha (s/ linhas centrais)
        tft.set_wifi_icon(width_max-16,height_max-16)                        # Coloca o icon wifi no display
        str6 = "%.2fV/" % (escalas_tensão[escala_tensão]/2)
        str7 = "%.2fHz/" % escalas_freq[escala_tempo]
        tft.display_write_str(tft.Arial16, str6, 0, height_max-16) #Apresenta a escala de tensão selecionada
        del str6
        tft.display_write_str(tft.Arial16, str7, 100, height_max-16) #Apresenta a escala de frequência selecionada
        del str7
        tft.display_nline(tft.MAGENTA, freq, spect_Xk)  #Imprime os pontos no osciloscópio

    return spect_Xk
        
def calc_Xk(pontos_volt):
    Xk=[0.0]*width_max
    real = 0
    Img = 0
    Xk_print = [0.0]*width_max
    
    for freq in range(round(width_max/2)):
        for i in range(width_max-1):
            real += pontos_volt[i] * math.cos((2*math.pi*freq*i)/width_max)   #Calcular a parte real da transformada de fourier
            Img += pontos_volt[i] * -math.sin(((2*math.pi*freq*i)/width_max)) #Calcular a parte imaginária da transformada de fourier
        Xk[2*freq] = math.sqrt((real**2) + (Img**2))  #Calcular o módulo da transformada de fourier
        Xk[(2*freq)+1] = Xk[2*freq]         #Cada ponto corresponde a dois pixeis
        Xk_print[2*freq] = (Xk[2*freq]/((escalas_tensão[escala_tensão]/2)/((height_max-16)/divisoes_y)))  #Converte o valor obtido para dar display
        Xk_print[(2*freq)+1] = Xk_print[2*freq]
        real=0
        Img=0
    gc.collect()
    del real, Img, Xk
    return Xk_print

def auto_scale(escala_tempo, escala_tensão):
    T=calc_periodo(escala_tempo)*1000 #Periodo em ms
    if(T == -1):
        return
    #Com o periodo, calcular a melhor escala horizontal (neste caso quermos mostrar 3 periodos)
    escala_tempo = calc_melhor_escala_hori(T)
    #Calcular a melhor escala vertical
    escala_tensão = calc_melhor_escala_verti()
    
    read_and_display(escala_tensão, escala_tempo,0, 1)
    
    return escala_tempo, escala_tensão
    
def calc_periodo(escala_tempo): #So funciona para ondas sinusoidais quadradas e triangulares
    indice_primeiro_pico = -1
    spect_Xk = calc_DFT(escala_tempo, escala_tensão, 0) #Calcula a DFT da onda periodica, para obter o seu primeiro pico (Que corresponde à sua frequencia).
    noise = 0.5

    for i in range(len(spect_Xk)-1): 
        if(spect_Xk[i+1]+noise < spect_Xk[i]): #Procura o primeiro pico de ampltiude
            indice_primeiro_pico = i
            break
    del spect_Xk, noise
    gc.collect()
    return 1 / ((escalas_freq[escala_tempo] / (width_max / divisoes_x)) * indice_primeiro_pico) #Cálculo do periodo 

def calc_melhor_escala_hori(T):
    tempo_periodos = T * 4 #tempo para se ver 3 períodos
    melhor_escala = 0
    
    for i in range(len(escalas_tempo)):
        if((escalas_tempo[i]*divisoes_x) < tempo_periodos): #Se o tempo de 3 períodos for maior que todo o eixo do tempo passamos para a escala seguinte
            continue
        else: #Se o tempo de 3 períodos for menor que todo o eixo do tempo
            melhor_escala = i
            break
    gc.collect()
    return melhor_escala

def calc_melhor_escala_verti():
    Vmax_module = 0
    tensao_max_escala = 0
    melhor_escala_vert = -1
    Vmax, Vmin, Vmed, Vrms, pontos_volt = read_and_display(escala_tensão, escala_tempo, 1,0) #Vamos calcular Vmax e Vmin
    del Vmed, Vrms, pontos_volt
    #Descobrir o maior valor em módulo
    if(Vmax > (-1*Vmin)):
        Vmax_module = Vmax
    else:
        Vmax_module = (-1*Vmin)

    del Vmax, Vmin
        
    for i in range(len(escalas_tensão)):
        tensao_max_escala = (escalas_tensão[i] * divisoes_y)/2 #Tensão máxima e mínima para cada escala
        if(Vmax_module > tensao_max_escala): #A escala é demasiado pequena para a tensão da onda
            continue
        else:
            melhor_escala_vert = i
            break
    gc.collect
    if(melhor_escala_vert == -1): #Se nenhuma chegar, escolhemos a maior escala
        melhor_escala_vert = 3 
        
    return melhor_escala_vert
            

# Programa principal (main)
escala_tempo = 2
escala_tensão = 3
fator = 1/29.3                                     # Fator do divisor resistivo
tft = T_Display.TFT()                              # Instancia um objeto da classe TFT
divisoes_x = 10
divisoes_y = 6
width_max = 240
height_max = 135
escalas_tempo = [5, 10, 20, 50]    #Escalas de tempo possíves em milisegundos
escalas_tensão = [1, 2, 5, 10]     #Escalas de tensão possíveis em volts
escalas_freq = [240, 120, 60, 24]
mail_to = "tiago.renou@tecnico.ulisboa.pt"


read_and_display(escala_tensão, escala_tempo,0, 1)

while tft.working():                              # Ciclo principal do programa
    but=tft.readButton()                          # Lê estado dos botões
    if but!=tft.NOTHING:
        if but==11:                               # Botão 1 clique rápido - Repete função
            read_and_display(escala_tensão, escala_tempo,0, 1)
            continue
        if but==12:                               # Botão 1 clique lento - Envia mail/Dá auto-scale/Efetua a calibração
            #calibrate_device()
            send_mail()
            #auto_scale(escala_tempo, escala_tensão)
            #read_and_display(escala_tensão, escala_tempo,0, 1)
            #escala_tempo, escala_tensão = auto_scale(escala_tempo, escala_tensão)
            continue
        if but==13:
            gc.collect                          #Botão 1 duplo clique - Demonstra os valores de Vmax, Vmin, Vmed e Vrms  
            volt_values()
            continue
        if but==21:                             #Botão 2 clique rapido - Altera o valor da escala de tensão
            escala_tensão = escala_tensão + 1
            if(escala_tensão >= len(escalas_tensão)):
                escala_tensão = 0
            read_and_display(escala_tensão, escala_tempo, 0,1)
            continue
        if but==22:                              #Botão 2 clique lento - Altera o valor da escala de tempo
            escala_tempo = escala_tempo + 1
            if(escala_tempo >= len(escalas_tempo)):
                escala_tempo= 0
            read_and_display(escala_tensão, escala_tempo, 0,1)
            continue
        if but==23:                              #Botão 2 duplo clique - Calcula e apresenta a FFT
            calc_DFT(escala_tempo, escala_tensão, 1)
            continue
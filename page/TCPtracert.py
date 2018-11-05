#!/usr/bin/env python
# -*- coding: utf-8 -*-
#A linha acima é necessária para indicar que a "leitura" para execução
#do arquivo seja feita naquela codificação (camada de Apresentação do OSI) 

import socket
import timeit

dest_host = input('IP Alvo: ')
max_hops = int(input('Quatidade de Saltos: '))
#portSrc = 0
portSrc = 33434
portDest = 80
icmp = socket.getprotobyname('icmp')
tcp = socket.getprotobyname('tcp')

#dest_host = '172.217.28.78' #Google
#dest_host = '8.8.8.8' #Google

dest_addr = (dest_host, portDest)
src_addr = ("", portSrc)#"" considera qualquer interface que possa escutar 'port'

ttl = 1

timei=None
timefTcp=None
timefIcmp=None

print ("TCPtracert to %s, port 80 (www)..." % (dest_host)) 
print ("TTL      T1      T2             Hostnome       IP Address ")

while True:

    print ("%d" % (ttl)),

    for x in range(0, 2):        
        #Abre socket de recebimento (a ordem de envio e recebimento é 
        #importante devido ao tempo de resposta)
       
        recv_socket_icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp) #receber só icmp

        #Associa o endereço local ao socket icmp de recebimento
        recv_socket_icmp.bind(src_addr)

        #"Seta" o tempo de espera por pacote/resposta em 's'
        recv_socket_icmp.settimeout(0.5)

        recv_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_RAW, tcp) #receber só tcp

        #Associa o endereço local ao socket TCP de recebimento        
        recv_socket_tcp.bind(src_addr)

        #"Seta o tempo de espera por pacote/resposta" em 's'
        recv_socket_tcp.settimeout(0.5)


        #Abre socket de envio
        send_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

        #Define o ttl no cabeçalho
        send_socket_tcp.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        send_socket_tcp.settimeout(0.5)

        #Envia o pedido de conexão TCP
        try: 
            send_socket_tcp.connect (dest_addr)
            timei = timeit.default_timer()
#           send_socket_tcp.settimeout(None)

        except socket.error:
	    # se for gerada a exceção aquele tempo não seria registrado
            timei = timeit.default_timer()
            #pass #Passa ignorando a necessidade de implementar o retorno        
            #print socket.error #[exceção 113]Haverá uma exceção quando, pelo menos, o ttl esgotar antes de o pacote chegar ao destino. Ou seja, se o destino não estiver no 1º salto

        curr_name = None
        curr_addrIcmp = None
        curr_addrTcp = None
        try:
            conn, curr_addrIcmp = recv_socket_icmp.recvfrom (1024)
            #Havendo exceção aqui, entender-se-á que não houve retorno. 
            #Uma consequência é a subtração (tempof-tempoi) resultar negativa. 
            #Sendo assim, um '*' será apresentado.           
            timefIcmp = timeit.default_timer() 
            curr_addrIcmp = curr_addrIcmp[0]

            try:
                curr_name = socket.gethostbyaddr(curr_addrIcmp)[0]

            except socket.error:
                curr_name = curr_addrIcmp              
        except socket.error:
            pass #Passa ignorando a necessidade de implementar o retorno        
            
        finally:
            #Closing connections
            recv_socket_icmp.close()
            send_socket_tcp.close()

        try:
            #Para verificar se o destino já foi alcançado e respondeu com TCP
            conn, curr_addrTcp = recv_socket_tcp.recvfrom (1024)
            timefTcp = timeit.default_timer()
            curr_addrTcp = curr_addrTcp[0]
            

        except socket.error:
            pass #Passa ignorando a necessidade de implementar o retorno        
        finally:
            #Closing connections
	        recv_socket_tcp.close()
           
	#A vírgula (em py 2.6) serve para omitir o \n "aguardando" nova
        #informação na mesma linha. Para py 3 tem outra forma. 

        if (timefIcmp is not None and timei is not None): 
            if (timefIcmp-timei)>=0:           
                print ("  %fms" % ((timefIcmp-timei)*1000)),
            else:
                print ("*" % ()),
        elif (timefTcp is not None and timei is not None): 
            if (timefTcp-timei)>=0:           
                print ("  %fms" % ((timefTcp-timei)*1000)),
            else:
                print ("*" % ()),
        else:
            print ("*" % ()),

    
    if (curr_addrTcp is not None and curr_addrTcp == dest_host) or ttl == max_hops:
        try:
            curr_name = socket.gethostbyaddr(curr_addrTcp)
        except socket.error:
            curr_name = curr_addrTcp
        print ("  %s [%s] " % (curr_name, curr_addrTcp))
        print ('\nRastreamento Concluído.' )  
        break
    else:
        print ("  %s [%s] " % (curr_name, curr_addrIcmp))
        ttl += 1
    
if curr_addrTcp != dest_host:
    print ("Destino %s não alcançado.\n" % (dest_host))


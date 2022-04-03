# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 20:53:48 2021

@author: mario
"""
import matplotlib.pyplot as plt

class SerieCSTR():
    
    def __init__(self,tau1,tau2,tau3,cain1,ka1,ka2,ka3):
        """Parâmetros fixos dos CSTRs em série"""
        self.tau1 = tau1
        self.tau2 = tau2
        self.tau3 = tau3
        self.cain1 = cain1
        self.ka1 = ka1
        self.ka2 = ka2
        self.ka3 = ka3
        """Vetores para plotagem dos gráficos"""
        self.ca1_plot = []
        self.ca2_plot = []
        self.ca3_plot = []
        self.tempo_plot = []
        
    """Funções auxiliares"""
    @staticmethod #indica que é uma função normal dentro de uma classe, por questão de organização.
    def __dca_dt(tau,c_in,c_out,k):
        "tau = tempo de residência (s)"
        "c_in = concentração do componente j na corrente de entrada do reator (mol/m³)"
        "c_out = concentração do componente j na corrente de saída do reator (mol/m³)"
        "k = constante de velocidade da reação no reator (m³/s)"
        der_dt = ((1)/(tau))*(c_in-c_out+tau*(-k*c_out))
        return der_dt
    
    def __euler(self,t_final,h,ca1_init,ca2_init,ca3_init):
        "t_final = tempo final (s)"
        "h = passo do método (s)"
        "ca1_init = valor inicial da concentração de A no reator 1 (mol/m³)"
        "ca2_init = valor inicial da concentração de A no reator 2 (mol/m³)"
        "ca3_init = valor inicial da concentração de A no reator 3 (mol/m³)"
        t = 0
        ca1n = ca1_init
        ca2n = ca2_init
        ca3n = ca3_init
        self.ca1_plot.append(ca1n)
        self.ca2_plot.append(ca2n)
        self.ca3_plot.append(ca3n)
        self.tempo_plot.append(t)
        while t < t_final:
            ca1n1 = ca1n + h*self.__dca_dt(self.tau1,self.cain1,ca1n,self.ka1)
            ca2n1 = ca2n + h*self.__dca_dt(self.tau2,ca1n,ca2n,self.ka2)
            ca3n1 = ca3n + h*self.__dca_dt(self.tau3,ca2n,ca3n,self.ka3)
            ca1n = ca1n1
            ca2n = ca2n1
            ca3n = ca3n1
            t = t + h
            self.ca1_plot.append(ca1n)
            self.ca2_plot.append(ca2n)
            self.ca3_plot.append(ca3n)
            self.tempo_plot.append(t)
    
    def __euler_din(self,t_final,h,ca1_init,ca2_init,ca3_init,t_pert,ca_pert):
        "t_final = tempo final (s)"
        "h = passo do método (s)"
        "ca1_init = valor inicial da concentração de A no reator 1 (mol/m³)"
        "ca2_init = valor inicial da concentração de A no reator 2 (mol/m³)"
        "ca3_init = valor inicial da concentração de A no reator 3 (mol/m³)"
        "t_pert = tempo de inicio da perturbação (s)"
        "porc_pert = porcentagem de perturbação da corrente de entrada"
        t = 0
        ca1n = ca1_init
        ca2n = ca2_init
        ca3n = ca3_init
        self.ca1_plot.append(ca1n)
        self.ca2_plot.append(ca2n)
        self.ca3_plot.append(ca3n)
        self.tempo_plot.append(t)
        "perturbação da concentração de A na corrente de entrada"
        while t < t_final:
            if t < t_pert:
                ca1n1 = ca1n + h*self.__dca_dt(self.tau1,self.cain1,ca1n,self.ka1)
                ca2n1 = ca2n + h*self.__dca_dt(self.tau2,ca1n,ca2n,self.ka2)
                ca3n1 = ca3n + h*self.__dca_dt(self.tau3,ca2n,ca3n,self.ka3)
                ca1n = ca1n1
                ca2n = ca2n1
                ca3n = ca3n1
                t = t + h
                self.ca1_plot.append(ca1n)
                self.ca2_plot.append(ca2n)
                self.ca3_plot.append(ca3n)
                self.tempo_plot.append(t)
                
            elif t >= t_pert:
                self.cain1 = ca_pert
                ca1n1 = ca1n + h*self.__dca_dt(self.tau1,self.cain1,ca1n,self.ka1)
                ca2n1 = ca2n + h*self.__dca_dt(self.tau2,ca1n,ca2n,self.ka2)
                ca3n1 = ca3n + h*self.__dca_dt(self.tau3,ca2n,ca3n,self.ka3)
                ca1n = ca1n1
                ca2n = ca2n1
                ca3n = ca3n1
                t = t + h
                self.ca1_plot.append(ca1n)
                self.ca2_plot.append(ca2n)
                self.ca3_plot.append(ca3n)
                self.tempo_plot.append(t)
                
    """Bloco que faz tudo"""
    def relatorio_estac(self,t_final,h,ca1_init,ca2_init,ca3_init):
        
        self.ca1_plot.clear()
        self.ca2_plot.clear()
        self.ca3_plot.clear()
        self.tempo_plot.clear()
        
        self.__euler(t_final,h,ca1_init,ca2_init,ca3_init)

        #plotagem do gráfico
        fig, graf = plt.subplots()
        #suplot Ca no reator 1
        graf.plot(self.tempo_plot,self.ca1_plot,label='Ca1 (mol/m³)')
        #subplot de Ca no reator 2
        graf.plot(self.tempo_plot,self.ca2_plot,label='Ca2 (mol/m³)')
        #subplot de Ca no reator 3
        graf.plot(self.tempo_plot,self.ca3_plot,label='Ca3 (mol/m³)')
        graf.set_xlabel('tempo (s)')
        graf.set_ylabel('Ca (mol/m³)')
        graf.set_title('Avaliação das concentrações com o tempo')
        graf.legend(loc = 'upper right')
        
        ca1_estac = str(self.ca1_plot[-1])
        ca2_estac = str(self.ca2_plot[-1])
        ca3_estac = str(self.ca3_plot[-1])
        
        print('-------------Relatório CSTRs em série-----------------')
        print('Para o estado estacionário, temos:')
        print('Concentração de A no reator 1 = '+ca1_estac)
        print('Concentração de A no reator 2 = '+ca2_estac)
        print('Concentração de A no reator 3 = '+ca3_estac)
        print('------------------------------------------------------')
    
    def relatorio_din(self,t_final,h,ca1_init,ca2_init,ca3_init,t_pert,porc_pert):
        
        ca_pert = ((porc_pert)/(100))*self.cain1 + self.cain1
        
        self.ca1_plot.clear()
        self.ca2_plot.clear()
        self.ca3_plot.clear()
        self.tempo_plot.clear()
        
        self.__euler_din(t_final,h,ca1_init,ca2_init,ca3_init,t_pert,ca_pert)
        #plotagem do gráfico
        fig, graf = plt.subplots()
        #suplot Ca no reator 1
        graf.plot(self.tempo_plot,self.ca1_plot,label='Ca1 (mol/m³)')
        #subplot de Ca no reator 2
        graf.plot(self.tempo_plot,self.ca2_plot,label='Ca2 (mol/m³)')
        #subplot de Ca no reator 3
        graf.plot(self.tempo_plot,self.ca3_plot,label='Ca3 (mol/m³)')
        graf.set_xlabel('tempo (s)')
        graf.set_ylabel('Ca (mol/m³)')
        graf.set_title('Avaliação das concentrações com o tempo')
        graf.legend(loc = 'upper right')
        
        ca1_estac = str(self.ca1_plot[-1])
        ca2_estac = str(self.ca2_plot[-1])
        ca3_estac = str(self.ca3_plot[-1])
        
        print('-------------Relatório CSTRs em série-----------------')
        print('Para uma perturbação de '+str(porc_pert)+'% na concentração de a na entrada do reator 1, temos:')
        print('Concentração de A no reator 1 = '+ca1_estac)
        print('Concentração de A no reator 2 = '+ca2_estac)
        print('Concentração de A no reator 3 = '+ca3_estac)
        print('------------------------------------------------------')
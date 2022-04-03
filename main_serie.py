# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 21:31:08 2021

@author: mario
"""
from cstrserie import SerieCSTR
tau1 = 2
tau2 = 2
tau3 = 2
cain1 = 1.8
ka1 = 0.5
ka2 = 0.5
ka3 = 0.5
reator1 = SerieCSTR(tau1,tau2,tau3,cain1,ka1,ka2,ka3)
t_final = 35
h = 0.001
ca1_init = 0.7
ca2_init = 0.5
ca3_init = 0.2
reator1.relatorio_estac(t_final,h,ca1_init,ca2_init,ca3_init)
t_pert = 20 #tempo de inicio da perturbação
porc_pert = -10 #porcentagem de perturbação
reator1.relatorio_din(t_final,h,ca1_init,ca2_init,ca3_init,t_pert,porc_pert)

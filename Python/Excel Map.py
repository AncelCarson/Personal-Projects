from mpl_toolkits import mplot3d
#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111,projection = '3d')

x = [1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8,8,8,8,8,8,9,9,9,9,9,9,9,9,9,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,11,11,11,11,11,11,11,11,11,11,11,11,11,12,12,12,12,12,12,12,12,12,12,12,12,12,13,13,13,13,13,13,13,13,13,13,13,13,13,14,14,14,14,14,14,14,14,14,14,14,14,14,15,15,15,15,15,15,15,15,15,15,15,15,15,16,16,16,16,16,16,16,16,16,16,16,16,16,17,17,17,17,17,17,17,17,17,17,17,17,17,18,18,18,18,18,18,18,18,18,18,18,18,18,19,19,19,19,19,19,19,19,19,19,19,19,19,20,20,20,20,20,20,20,20,20,20,20,20,20,]
y = [1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,1,2,3,4,5,6,7,8,9,10,11,12,13,]
z = [8.68903340911164,10.7053060955549,10.6420040113693,7.94626438058061,11.0827130405319,8.4207474847991,6.90700132349689,8.37453818565795,6.75382434721649,8.93721410786319,11.103380187206,9.7105388031106,9.30935504666288,8.32236580939418,7.01078928898744,11.9397299454628,11.056437985655,11.2264381258811,10.3282877209438,8.45563011571772,10.3608145270975,10.4690527491545,6.21161762701549,9.95942927746635,10.9735839091214,11.2968029824696,9.18658783453058,9.9224151184439,9.57701810726866,9.30660061124027,9.67314434561157,14.6193780386702,9.13271340889868,5.97106681503122,11.202088010713,12.1390773843191,8.85923563342292,9.75367850068102,13.2593399968459,12.9888378895046,10.9540762872713,8.90602712317501,8.85438318335482,9.68624207072739,8.92798132780367,8.36760010969889,11.9043971503996,5.04930753243862,9.51182011596992,8.69585320684974,9.32573321945813,8.01311955376305,8.77866412033421,10.0430239344665,8.86241213495435,15.0615044675788,12.4437726271179,7.63754741339651,10.793803846545,8.08172561744067,9.28029400358787,12.3881282613275,7.31618668453882,12.6032143101566,8.90725782631138,9.09214525765387,9.39565345247699,8.47556950140494,9.68621623604409,11.2339570622817,12.0595994433727,9.93646345627597,7.85501286775646,14.0026249048657,7.79870499624561,11.8234147807789,9.92759687622617,10.7318981689937,9.50952600804444,9.67629398320774,12.4912098218673,11.7602650631948,8.46605184455065,8.09988327019875,14.9333354887966,10.1165261754657,11.5043991515637,11.8946269136397,9.50491863707118,10.5786917455811,13.8796831787132,7.42852340607486,12.399175910902,7.3371057644285,8.50194303709274,11.2440952226811,12.1203224787545,10.3411798736729,7.57392757587234,9.82144791773901,13.8699786620045,7.04612329367407,10.5000686330208,8.15899346410122,9.98909733231581,14.249223828323,9.12572467040329,6.58161384289681,7.98288168142976,10.7102664545866,10.9809941454056,7.79263677547383,9.05086051194139,8.56106215370976,11.7513104703793,9.18932934790629,8.72244968947628,11.4782448600636,12.1606084608619,10.3278015043028,8.9436373780175,9.30923591730061,10.6450853225357,7.48280666638456,11.7448362039229,8.94985453895328,7.1775038698361,7.83356911873824,8.17410048805562,10.5580453050695,9.0968220028571,10.6685189406722,9.84323600536185,6.38446932487433,13.3153158751737,8.87421443183579,9.06302926620908,10.3450179623576,9.80263451133473,11.0305923804318,11.6856995421212,11.7851233029295,13.5215025368255,12.2766984757697,13.5516104327935,10.8585400923588,12.1223199462995,10.6146142399316,8.94006496510265,8.86609334373817,9.66691818888139,9.80882722481532,11.7000950717324,9.32645020615111,9.39354246874339,10.9867548453465,9.22584611514185,9.79144801387429,12.4920763218005,12.2339834420236,10.64210376678,9.34423328453241,13.3637760337817,13.4233233903814,9.57914963043704,11.2313984136679,7.92116409762586,11.9783055191303,11.3699970598809,10.4228737007376,9.03262689059103,12.6822812108775,9.52048707905782,6.97670628632323,10.7409387555864,10.3830853196801,12.4891129091443,8.28558211877246,10.4767243524154,9.3759403384743,14.4842043241498,12.8380865324885,8.65904904588474,9.76477543592684,11.222369148485,10.1962570057898,10.1868464302331,11.5031214766266,11.2088594636771,12.0426994631356,12.2285440305303,8.76928448006758,7.31714274959331,12.4053665821797,8.89496935567492,9.01813355662766,11.7235046528515,9.74879677004916,7.2198183699278,9.74769153433813,8.42253621246001,10.3865551720919,9.13345197957005,7.96576193845878,8.35287187262718,11.402155358314,8.0597104731848,3.58174770764608,12.896585276639,11.6897932234631,8.64892851778731,9.99275111194424,7.79120441478382,7.97211641691534,9.61023267902729,9.98773551843292,11.8290235401747,8.40140929467821,9.96027207817904,8.28087758339836,13.1484314009106,8.50745859350075,11.0950922239347,8.1429994664366,9.71267236658432,6.79981286816823,13.5108675505373,12.0635954320243,11.9203560796113,9.55612431827696,9.77654950843193,10.3355603352762,9.55534065704011,8.28164780416152,6.93338274862644,10.131300911056,13.719088612538,13.3012409033503,12.2549833045825,10.0115623026677,8.80833960850909,10.1406614070548,9.15914932867367,9.24721298270184,11.9962021764164,7.04926876109053,9.58190289988062,10.3675153066926,8.70568448695162,10.8487789855611,6.74406178914189,9.44368971626505,10.9711228105517,10.5114099653921,14.4152593487644,9.58938726810457,11.2023173536616,8.95357824573929,9.77950869548236,11.710048596,]

#ax.plot_trisurf(x,y,z, cmap = 'viridis', edgecolor = 'none')
#ax.plot_surface(x,y,z, cmap = 'viridis', edgecolor = 'none')
#ax.contour(x,y,z, cmap = 'viridis')
ax.tricontour(x,y,z)

plt.show()

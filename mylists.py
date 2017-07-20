#Unchanging lists

##Copyright (C) 2012 Magnus Haw
##
##This program is free software: you can redistribute it and/or modify
##it under the terms of the GNU General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU General Public License for more details.
##
##You should have received a copy of the GNU General Public License
##along with this program.  If not, see <http://www.gnu.org/licenses/>.

from numpy import array

con= array([['Hydra', 'Hya'],
       ['Virgo', 'Vir'],
       ['Ursa Major', 'UMa'],
       ['Cetus', 'Cet'],
       ['Hercules', 'Her'],
       ['Eridanus', 'Eri'],
       ['Pegasus', 'Peg'],
       ['Draco', 'Dra'],
       ['Centaurus', 'Cen'],
       ['Aquarius', 'Aqr'],
       ['Ophiuchus', 'Oph'],
       ['Leo', 'Leo'],
       ['Bootes', 'Boo'],
       ['Pisces', 'Psc'],
       ['Sagittarius', 'Sgr'],
       ['Cygnus', 'Cyg'],
       ['Taurus', 'Tau'],
       ['Camelopardalis', 'Cam'],
       ['Andromeda', 'And'],
       ['Puppis', 'Pup'],
       ['Auriga', 'Aur'],
       ['Aquila', 'Aql'],
       ['Serpens', 'Ser'],
       ['Perseus', 'Per'],
       ['Cassiopeia', 'Cas'],
       ['Orion', 'Ori'],
       ['Cepheus', 'Cep'],
       ['Lynx', 'Lyn'],
       ['Libra', 'Lib'],
       ['Gemini', 'Gem'],
       ['Cancer', 'Cnc'],
       ['Vela', 'Vel'],
       ['Scorpius', 'Sco'],
       ['Carina', 'Car'],
       ['Monoceros', 'Mon'],
       ['Sculptor', 'Scl'],
       ['Phoenix', 'Phe'],
       ['Canes Venatici', 'CVn'],
       ['Aries', 'Ari'],
       ['Capricornus', 'Cap'],
       ['Fornax', 'For'],
       ['Coma Berenices', 'Com'],
       ['Canis Major', 'CMa'],
       ['Pavo', 'Pav'],
       ['Grus', 'Gru'],
       ['Lupus', 'Lup'],
       ['Sextans', 'Sex'],
       ['Tucana', 'Tuc'],
       ['Indus', 'Ind'],
       ['Octans', 'Oct'],
       ['Lepus', 'Lep'],
       ['Lyra', 'Lyr'],
       ['Crater', 'Crt'],
       ['Columba', 'Col'],
       ['Vulpecula', 'Vul'],
       ['Ursa Minor', 'UMi'],
       ['Telescopium', 'Tel'],
       ['Horologium', 'Hor'],
       ['Pictor', 'Pic'],
       ['Piscis Austrinus', 'PsA'],
       ['Hydrus', 'Hyi'],
       ['Antlia', 'Ant'],
       ['Ara', 'Ara'],
       ['Leo Minor', 'LMi'],
       ['Pyxis', 'Pyx'],
       ['Microscopium', 'Mic'],
       ['Apus', 'Aps'],
       ['Lacerta', 'Lac'],
       ['Delphinus', 'Del'],
       ['Corvus', 'Crv'],
       ['Canis Minor', 'CMi'],
       ['Dorado', 'Dor'],
       ['Corona Borealis', 'CrB'],
       ['Norma', 'Nor'],
       ['Mensa', 'Men'],
       ['Volans', 'Vol'],
       ['Musca', 'Mus'],
       ['Triangulum', 'Tri'],
       ['Chamaeleon', 'Cha'],
       ['Corona Australis', 'CrA'],
       ['Caelum', 'Cae'],
       ['Reticulum', 'Ret'],
       ['Triangulum Australe', 'TrA'],
       ['Scutum', 'Sct'],
       ['Circinus', 'Cir'],
       ['Sagitta', 'Sge'],
       ['Equuleus', 'Equ'],
       ['Crux', 'Cru']], 
      dtype='<U19')

otypes = array([['Open Cluster','OCl'],
 ['Globular Cluster', 'GCl'],
 ['Planetary Nebula', 'PlNeb'],
 ['Starforming Nebula', 'SfNeb'],
 ['Spiral Galaxy', 'SGal'],
 ['Elliptical Galaxy', 'EGal'],
 ['Irregular Galaxy', 'IrGal'],
 ['Lenticular (S0) Galaxy', 'LGal'],
 ['Supernova Remnant', 'SNova'],
 ['Multiple Star sytem', 'Mul'],
 ['Other', 'Other'],
 ['Binary star', 'Bin']],dtype='<U19')

objectcols =[
        'name',
        'id ',
        'type',
        'magnitude',
        'size',
        'distance_kly',
        'constellation',
        'RA',
        'dec',
        'finding_chart',
        'image',
        'description',
        'other_names',
        'link',
        'comments']

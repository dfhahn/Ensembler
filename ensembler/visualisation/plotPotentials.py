import os, sys
import numpy as np
import matplotlib
from matplotlib import pyplot as plt, colorbar
from typing import Tuple, List
from numbers import Number
import ensembler.potentials.TwoD as pot2D


SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

cmap = "tab20b"

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


from ensembler.potentials import OneD as pot, ND as nDPot
from ensembler.potentials._baseclasses import _potential1DCls, _perturbedPotentialNDCls

#UTIL FUNCTIONS
def significant_decimals(s:float)->float:
    significant_decimal=2
    if(s % 1 != 0):
        decimals = str(float(s)).split(".")[-1]
        for digit in decimals:
            if(digit == "0"):
                significant_decimal +=1
            else:
                return round(s, significant_decimal)
    else:
        return s

def plot_1DPotential(potential: _potential1DCls, positions:list,
                     x_range=None, y_range=None, title:str=None, ax=None):
    # generat Data
    energies = potential.ene(positions=positions)

    # is there already a figure?
    if (ax == None):
        fig = plt.figure()
        ax = fig.add_subplot(111)
    else:
        fig = None

    # plot
    ax.plot(positions, energies)
    ax.set_xlim(min(x_range), max(x_range)) if (x_range!=None) else ax.set_xlim(min(positions), max(positions))
    ax.set_ylim(min(y_range), max(y_range)) if (y_range!=None) else ax.set_ylim(min(energies), max(energies))

    ax.set_xlabel('$x$')
    ax.set_ylabel('$Potential [kj]$')
    ax.set_title(title) if (title != None) else ax.set_title("Potential "+str(potential.name))

    if(ax != None):
        return fig, ax
    else:
        return ax
    pass

def plot_1DPotential_dhdpos(potential: _potential1DCls, positions:list,
                            x_range=None, y_range=None, title:str=None, ax=None):
    # generat Data
    energies = potential.dvdpos(positions=positions)

    # is there already a figure?
    if (ax == None):
        fig = plt.figure()
        ax = fig.add_subplot(111)
    else:
        fig = None

    # plot
    ax.plot(positions, energies)
    ax.set_xlim(min(x_range), max(x_range)) if (x_range!=None) else ax.set_xlim(min(positions), max(positions))
    ax.set_ylim(min(y_range), max(y_range)) if (y_range!=None) else ax.set_ylim(min(energies), max(energies))

    ax.set_xlabel('$x$')
    ax.set_ylabel('$Potential [kj]$')
    ax.set_title(title) if (title != None) else ax.set_title("Potential "+str(potential.name))

    if(ax != None):
        return fig, ax
    else:
        return ax
    pass


def plot_1DPotential_Term(potential:_potential1DCls, positions: list,
                          x_range=None, y_range=None, title: str = None, ax=None):
    fig, axes = plt.subplots(nrows=1, ncols=2)
    plot_1DPotential(potential=potential, positions=positions, ax=axes[0], x_range=x_range, y_range=y_range, title="Pot")
    plot_1DPotential_dhdpos(potential=potential, positions=positions, ax=axes[1], x_range=x_range, y_range=y_range, title="dhdpos")
    fig.tight_layout()
    fig.suptitle(title) if(title!=None) else fig.suptitle("Potential "+str(potential.name))
    return fig, axes

def plot_1DPotential_Termoverlay(potential: _potential1DCls, positions:list,
                                 x_range=None, y_range=None, title: str = None, ax=None):
    #generate dat
    energies = potential.ene(positions=positions)
    dVdpos = potential.dhdpos(positions=positions)

    # is there already a figure?
    if (ax == None):
        fig = plt.figure()
        ax = fig.add_subplot(111)
    else:
        fig = None

    ax.plot(positions, energies, label="V")
    ax.plot(positions, list(map(abs, dVdpos)), label="absdVdpos")
    ax.plot(positions, dVdpos, label="dVdpos")
    ax.set_xlim(min(x_range), max(x_range)) if (x_range!=None) else ax.set_xlim(min(positions), max(positions))
    ax.set_ylim(min(y_range), max(y_range)) if (y_range!=None) else ax.set_ylim(min([min(energies), min(dVdpos)]), max([max(energies), max(dVdpos)]))

    ax.ylabel("$Potential/kJ$")
    ax.xlabel("$x$")
    ax.legend()
    ax.set_title(title) if (title != None) else ax.set_title("Potential "+str(potential.__name__))

    if(ax != None):
        return fig, ax
    else:
        return ax



"""
 2D Plotting Functions
"""
def plot_2DPotential(V:pot2D._potential2DClsSymPY, positions2D:List[Tuple[Number,Number]]=None, title:str=None, x_label:str=None, y_label:str=None, space_range:Tuple[Number, Number]=(-10, 10), point_resolution:int=1000, ax=None, show_plot:bool=False, dpi:int=300)->(plt.Figure, plt.Axes, np.array):
        #build positions
    if(isinstance(positions2D, type(None))):
        minX, maxX = min(space_range), max(space_range)
        minY, maxY = min(space_range), max(space_range)
        positions = np.linspace(min(space_range), max(space_range), point_resolution)
        x_positions, y_positions = np.meshgrid(positions,positions)
        positions2D = np.array([x_positions.flatten(), y_positions.flatten()]).T
    else:
        positions2D = np.array(positions2D)
        minX, maxX = min(positions2D[:,0]), max(positions2D[:,0])
        minY, maxY = min(positions2D[:,1]), max(positions2D[:,1])    

    #landscapes
    V_pots = V.ene(positions2D)
    minV,maxV = np.min(V_pots), np.max(V_pots)
    V_land = V_pots.reshape([point_resolution,point_resolution])

    #make Figure
    if(isinstance(ax, type(None))):
        fig, ax = plt.subplots(ncols=1, dpi=dpi)
    else:
        fig = None

    surf = ax.imshow(V_land, cmap="tab20b",  extent=[minX, maxX, minY, maxY])
    ax.set_xlabel("x")

    
    if(isinstance(x_label, type(None))):
        ax.set_xlabel("x")
    else:
        ax.set_xlabel(x_label)

        
    if(isinstance(y_label, type(None))):
        ax.set_ylabel("y")
    else:
        ax.set_ylabel(y_label)


    ax.set_xticks(np.linspace(minX, maxX+1, 5))
    ax.set_yticks(np.linspace(minY, maxY+1, 5))


    if(isinstance(title, type(None))):
        ax.set_title("Potential Landscape")
    else:
        ax.set_title(title)

    #color bar:
    if(not isinstance(fig, type(None))):
        cbaxes = fig.add_axes([0.9, 0.1, 0.03, 0.8]) 
        cb = plt.colorbar(surf, fraction=0.046, pad=0.04, cax = cbaxes, ticks=list(np.round(np.linspace(minV,maxV,5),2)))
        cb.set_label("V/[kT]")

        fig.tight_layout()
        
        if(show_plot):
            fig.show()

    return fig, ax, surf


def plot_2DEnergy_landscape(potential1: _potential1DCls, potential2: _potential1DCls, positions1:list, positions2:list=None,
                            x_range=None, y_range=None, z_range=None, title:str=None, colbar:bool=False, ax=None, cmap:str="inferno"):
    #generat Data
    energy_map = []
    min_E, max_E = 0,0

    if(type(positions2)==type(None)):
        positions2 = positions1

    for pos in positions2:
        Va = potential2.ene(pos)[0]
        Vb = potential1.ene(positions1)
        Vtot = list(map(lambda x: x+Va, Vb))
        energy_map.append(Vtot)

        if(min(Vtot)<min_E):
            min_E = min(Vtot)
        if(max(Vtot)>max_E):
            max_E = max(Vtot)

    energy_map = np.array(energy_map)

    #is there already a figure?
    if(ax == None):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        colbar=True
    else:
        fig = None

    if(z_range==None):
        z_range = [min_E, max_E]

    #plot
    surf = ax.imshow(energy_map, cmap=cmap, interpolation="nearest",
                     origin='center', extent=[min(positions1), max(positions1), min(positions2), max(positions2)],  vmax=max(z_range), vmin=min(z_range), aspect="auto")

    if(colbar and fig != None):
        fig.colorbar(surf, aspect=5, label='Energy/kJ')

    if(x_range): ax.set_xlim(min(x_range), max(x_range))
    if(y_range): ax.set_ylim(min(y_range), max(y_range))

    ax.set_xlabel('$x1$')
    ax.set_ylabel('$x2$')
    if(title): ax.set_title(title)
    return fig, ax, surf

"""
 MultiState Plotting Functions
"""
#1D

def plot_2perturbedEnergy_landscape(potential:_perturbedPotentialNDCls, positions:list, lambdas:list,
                                    x_range=None, lam_range=None, title:str=None, colbar:bool=False, ax=None):

    energy_map_lin = []
    for y in lambdas:
        potential.set_lam(y)
        energy_map_lin.append(potential.ene(positions))
    energy_map_lin = np.array(energy_map_lin)

    if(ax == None):
        fig = plt.figure(figsize=(15,5))
        ax = fig.add_subplot(111)
        colbar=True
    else:
        fig = None

    surf = ax.imshow(energy_map_lin, cmap="viridis", interpolation="nearest",
                     origin='center', extent=[min(positions), max(positions), min(lambdas), max(lambdas)],  vmax=100, vmin=0, aspect="auto")

    if(colbar):
        colorbar.Colorbar(ax, surf, label='Energy')

    if(x_range): ax.set_xlim(min(x_range), max(x_range))
    if(lam_range): ax.set_ylim(min(lam_range), max(lam_range))
    ax.set_xlabel('x')
    ax.set_ylabel('$\lambda$')
    if(title): ax.set_title(title)
    return fig, ax, surf

#show feature landscape per s
def envPot_differentS_overlay_min0_plot(eds_potential:nDPot.envelopedPotential, s_values:list, positions:list,
                                        y_range:tuple=None, hide_legend:bool=False, title:str=None, out_path:str=None):
    #generate energy values
    ys = []
    scale = 1 # 0.1
    for s in s_values:
        eds_potential.s=s
        enes = eds_potential.ene(positions)
        y_min =min(enes)
        y=list(map(lambda z: (z-y_min)*scale, enes))
        ys.append(y)

    #plotting
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(20,10))
    for s, y in reversed(list(zip(s_values, ys))):
        axes.plot(positions, y, label="s_"+str(significant_decimals(s)))

    if (y_range != None):
        axes.set_ylim(y_range)
    axes.set_xlim(min(positions),max(positions))

    #styling
    axes.set_ylabel("Vr/[kJ]")
    axes.set_xlabel("r")
    axes.set_title("different Vrs aligned at 0 with different s-values overlayed ")

    ##optionals
    if(not hide_legend): axes.legend()
    if(title):    fig.suptitle(title)
    if(out_path): fig.savefig(out_path)
    fig.show()

    return fig, axes

#show feature landscape per s
def envPot_differentS_overlay_plot(eds_potential:nDPot.envelopedPotential, s_values:list, positions:list,
                                   y_range:tuple=None, hide_legend:bool=False, title:str=None, out_path:str=None, axes=None):
    #generate energy values
    ys = []
    for s in s_values:
        eds_potential.s=s
        enes = eds_potential.ene(positions)
        ys.append(enes)

    #plotting
    if(axes == None):
        fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(20,10))
    else:
        fig = None

    for s, y in reversed(list(zip(s_values, ys))):
        axes.plot(positions, y, label="s_"+str(significant_decimals(s)))

    #styling
    axes.set_xlim(min(positions),max(positions))
    axes.set_ylabel("Vr/[kJ]")
    axes.set_xlabel("r")
    if(title ==None):
        axes.set_title("different $V_{r}$s with different s-values overlayed ")
    else:
        axes.set_title(title)


    ##optionals
    if (y_range != None): axes.set_ylim(y_range)
    if(not hide_legend): axes.legend()
    if(title and not isinstance(fig, type(None))):    fig.suptitle(title)
    if(out_path and not isinstance(fig, type(None))): fig.savefig(out_path)
    if(not isinstance(fig, type(None))): fig.show()

    return fig, axes

def envPot_diffS_compare(eds_potential:nDPot.envelopedPotential, s_values:list, positions:list,
                         y_range:tuple=None,title:str=None, out_path:str=None):
    ##row/column ratio
    per_row =4
    n_rows = (len(s_values)//per_row)+1 if ((len(s_values)%per_row)>0) else (len(s_values)//per_row)

    ##plot
    fig, axes = plt.subplots(nrows=n_rows, ncols=per_row, figsize=(20,10))
    axes = [ax for ax_row in axes for ax in ax_row]

    for ax, s in zip( axes, s_values):
        eds_potential.s=s
        y=eds_potential.ene(positions)
        ax.plot(positions, y)

        #styling
        ax.set_xlim(min(positions), max(positions))
        ax.set_title("s_"+str(significant_decimals(s)))
        ax.set_ylabel("Vr/[kJ]")
        ax.set_xlabel("r")
        if (y_range != None): ax.set_ylim(y_range)

    ##optionals
    if(title):    fig.suptitle(title)
    if(out_path): fig.savefig(out_path)
    fig.show()
    return fig, axes

def plot_envelopedPotential_system(eds_potential:nDPot.envelopedPotential, positions:list, s_value:float=None, Eoffi:list=None,
                                   y_range:tuple=None,title:str=None, out_path:str=None):
    if(s_value!=None):
        eds_potential.s = s_value       #set new s
    if(Eoffi!=None):
        if(len(Eoffi) == len(eds_potential.V_is)):
            eds_potential.Eoff_i = Eoffi
        else:
            raise IOError("There are "+str(len(eds_potential.V_is))+" states and "+str(Eoffi)+", but the numbers have to be equal!")

    ##calc energies
    energy_Vr = eds_potential.ene(positions)
    energy_Vis = [state.ene(positions) for state in eds_potential.V_is]
    num_states = len(eds_potential.V_is)

    ##plot nicely
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
    axes = [ax for ax_row in axes for ax in ax_row]
    y_values = energy_Vis + [energy_Vr]
    labels = ["state_"+str(ind) for ind in range(1,len(energy_Vis)+1)]+["refState"]

    for ax, y, label in zip(axes, y_values, labels):
        ax.plot(positions, y)
        ax.set_xlim(min(positions), max(positions))
        ax.set_ylim(y_range)
        ax.set_title(label)
        ax.set_ylabel("Vr/[kJ]")
        ax.set_xlabel("r_"+label)

    ##optionals
    if(title):    fig.suptitle(title)
    if(out_path): fig.savefig(out_path)
    fig.show()
    return fig, axes

def plot_envelopedPotential_2State_System(eds_potential: nDPot.envelopedPotential, positions:list, s_value:float=None, Eoffi:list=None,
                                          title:str=None, out_path:str=None, V_max:float=600, V_min:float=None):

    if(len(eds_potential.V_is)>2):
        raise IOError(__name__+" can only be used with two states in the potential!")

    if(s_value!=None):
        eds_potential.s = s_value

    if (Eoffi != None):
        if (len(Eoffi) == len(eds_potential.V_is)):
            eds_potential.Eoff_i = Eoffi
        else:
            raise IOError("There are " + str(len(eds_potential.V_is)) + " states and " + str(
                Eoffi) + ", but the numbers have to be equal!")

    #Calculate energies
    energy_Vr = eds_potential.ene(positions)
    energy_Vis = [state.ene(positions) for state in eds_potential.V_is]
    energy_map = []
    min_e = 0

    for x in positions:
        row = eds_potential.ene(list(map(lambda y:[[x], [y]], list(positions))))
        row_cut = list(map(lambda x:  V_max if(V_max != None and float(x) > V_max) else float(x), row))
        energy_map.append(row_cut)
        if(min(row)< min_e):
            min_e=min(row)

    if(V_min==None):
        V_min=min_e

    ##plot nicely
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
    axes = [ax for ax_row in axes for ax in ax_row]
    y_values = energy_Vis + [energy_Vr]
    labels = ["State_" + str(ind) for ind in range(1, len(energy_Vis) + 1)] + ["State_R"]

    #plot the line potentials
    colors = ["steelblue", "orange", "forestgreen"]
    for ax, y, label,c in zip(axes, y_values, labels,colors):
        ax.plot(positions, y, c)
        ax.set_xlim(min(positions), max(positions))
        ax.set_ylim([V_min, V_max])
        ax.set_title("Potential $"+label+"$")
        ax.set_ylabel("$V/[kJ]$")
        ax.set_xlabel("$r_{ " + label+"} $")

    #plot phase space surface
    ax = axes[-1]
    surf = ax.imshow(energy_map, cmap="inferno", interpolation="nearest",
                    origin='center', extent=[min(positions), max(positions), min(positions), max(positions)],
                     vmax=V_max, vmin=V_min)
    ax.set_xlabel("$r_{"+labels[0]+"}$")
    ax.set_ylabel("$r_{"+labels[1]+"}$")
    ax.set_title("complete phaseSpace of $state_R$")
    #fig.colorbar(surf, aspect=5, label='Energy/kJ')

    ##optionals
    if(title):    fig.suptitle(title)
    if(out_path): fig.savefig(out_path)
    fig.show()
    return fig, axes


def envPot_diffS_2stateMap_compare(eds_potential: pot.envelopedPotential, s_values: list, positions: list,
                                   V_max: float = 500, V_min: float = None, title: str = None, out_path: str = None):
    ##row/column ratio
    per_row = 4
    n_rows = (len(s_values) // per_row) + 1 if ((len(s_values) % per_row) > 0) else (len(s_values) // per_row)

    ##plot
    fig, axes = plt.subplots(nrows=n_rows, ncols=per_row, figsize=(20, 10))
    axes = [ax for ax_row in axes for ax in ax_row]
    first = True

    for ax, s in zip(axes, s_values):
        eds_potential.s = s
        min_e = 0
        energy_map = []
        for x in positions:
            row = eds_potential.ene(list(map(lambda y: [[x], [y]], list(positions))))
            row_cut = list(map(lambda x: V_max if (V_max != None and float(x) > V_max) else float(x), row))
            energy_map.append(row_cut)
            if (min(row) < min_e):
                min_e = min(row)

        if (V_min == None and first):
            V_min = min_e
            first = False
            print("emin: ", min_e)

        # plot phase space surface
        surf = ax.imshow(energy_map, cmap="viridis", interpolation="nearest",
                         origin='center', extent=[min(positions), max(positions), min(positions), max(positions)],
                         vmax=V_max, vmin=V_min)
        ax.set_xlabel("$r_1$")
        ax.set_ylabel("$r_2$")
        ax.set_title("complete phaseSpace of $state_R$")
    fig.colorbar(surf, aspect=10, label='Energy/kJ')

    ##optionals
    if (title):    fig.suptitle(title)
    if (out_path): fig.savefig(out_path)
    fig.show()

    return fig, axes


#2D


"""
 Wrappers for special Cases
"""
def plot_2D_2states(V1, V2,  space_range:Tuple[Number, Number]=None):
    fig, axes = plt.subplots(ncols=2, figsize=[15,10])
    _, ax1, surf1 = plot_2DPotential(V1, ax=axes[0], title="State 1", x_label="$\phi/[^{\circ}]$", y_label="$\psi/[^{\circ}]$", space_range=space_range)
    _, ax2, surf2 = plot_2DPotential(V2, ax=axes[1], title="State 2", x_label="$\phi/[^{\circ}]$", y_label="$\psi/[^{\circ}]$", space_range=space_range)

    #color bar:
    cbaxes = fig.add_axes([ax2.get_position().x1*1.15,  ax2.get_position().y0, 0.03, ax2.get_position().height]) 
    cb = plt.colorbar(surf2 , cax = cbaxes, ticks=list(np.round(np.linspace(np.min(surf1._A),np.max(surf1._A),5),2)),)
    cb.set_label("V/[kT]")
    fig.tight_layout()

    fig.suptitle("The Two End States for EDS Potential",  y=0.9)

    return fig

def plot_2D_2State_EDS_potential(eds_pot, out_path:str=None, traj=None, s=100, positions2D=None, space_range=[-180, 180], point_resolution=500, x_label="$\phi/[^{\circ}$]", y_label="$\psi/[^{\circ}$]", verbose=False):
    traj_color = "orange"
    
    #build positions
    if(isinstance(positions2D, type(None))):
        minX, maxX = min(space_range), max(space_range)
        minY, maxY = min(space_range), max(space_range)
        positions = np.linspace(min(space_range), max(space_range), point_resolution)
        x_positions, y_positions = np.meshgrid(positions,positions)
        positions2D = np.array([x_positions.flatten(), y_positions.flatten()]).T
    else:
        positions2D = np.array(positions2D)
        point_resolution=len(np.unique(positions2D[:,0]))
        minX, maxX = min(positions2D[:,0]), max(positions2D[:,0])
        minY, maxY = min(positions2D[:,1]), max(positions2D[:,1])   

    #calc energies for total space
    #subPotentials
    eds_pot.s = s
    V1 = eds_pot.V_is[0]
    V2 = eds_pot.V_is[1]
    #Energies
    energies1 = V1.ene(positions2D)
    energies2 = V2.ene(positions2D)
    energiesEds = eds_pot.ene(positions2D)

    #generate map for 2D
    if(verbose): print("map data")
    energies1Map = energies1.reshape([point_resolution, point_resolution])
    energies2Map = energies2.reshape([point_resolution, point_resolution])
    energiesEdsMap = energiesEds.reshape([point_resolution, point_resolution])

    #plotting
    if(verbose): print("plot")
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=[15,6], dpi=300)

    minV,maxV = np.min(energies1Map), np.max(energies1Map)
    surf1 = ax1.imshow(energies1Map, cmap=cmap, interpolation="nearest", origin='center', vmax=maxV, vmin=minV, extent=[minX, maxX, minY, maxY])
    surf2 = ax2.imshow(energies2Map, cmap=cmap, interpolation="nearest", origin='center', vmax=maxV, vmin=minV, extent=[minX, maxX, minY, maxY])   

    minV,maxV = np.min(energies1), np.max(energies1)
    surf3 = ax3.imshow(energiesEdsMap, cmap=cmap, interpolation="nearest", origin='center', vmax=maxV, vmin=minV, extent=[minX, maxX, minY, maxY])
    
    #color bar:
    cbaxes = fig.add_axes([1.0, 0.1, 0.03, 0.8]) 
    cb = plt.colorbar(surf3 ,fraction=0.046, pad=0.04, cax = cbaxes, ticks=list(np.round(np.linspace(minV,maxV,5),2)))
    cb.set_label("V/[kT]")
    
    ##LAEBELLING FUN
    ax1.set_ylim([min(space_range),max(space_range)])
    ax2.set_ylim([min(space_range),max(space_range)])
    ax3.set_ylim([min(space_range),max(space_range)])
    
    ax1.set_xlim([min(space_range),max(space_range)])
    ax2.set_xlim([min(space_range),max(space_range)])
    ax3.set_xlim([min(space_range),max(space_range)])
    
    ax1.set_ylabel(y_label, fontsize=18)
    
    ax1.set_xlabel(x_label, fontsize=18)
    ax2.set_xlabel(x_label, fontsize=18)
    ax3.set_xlabel(x_label, fontsize=18)

    
    ax1.set_yticks([-180, -90, 0, 90, 180])
    ax2.set_yticks([])
    ax3.set_yticks([])
    ax1.set_xticks([-180, -90, 0, 90, 180])
    ax2.set_xticks([-180, -90, 0, 90, 180])
    ax3.set_xticks([-180, -90, 0, 90, 180])
    
    ax1.tick_params(labelsize=14)
    ax2.tick_params(labelsize=14)
    ax3.tick_params(labelsize=14)
    
    #put TRAJ in to landscape
    if(not isinstance(traj, type(None))):
        visited_positions = traj.position.values
        vis_pos_x, vis_pos_y =  np.array([state_positions[0] for state_positions in traj.position]).T

        ax1.scatter(vis_pos_x, vis_pos_y, c=traj_color, alpha=0.3)
        ax2.scatter(vis_pos_x, vis_pos_y, c=traj_color, alpha=0.3)
        ax3.scatter(vis_pos_x, vis_pos_y, c=traj_color, alpha=0.3)

        ax1.scatter(list(traj.position)[-1][0][0], list(traj.position)[-1][0][1], c="r")
        ax2.scatter(list(traj.position)[-1][0][0], list(traj.position)[-1][0][1], c="r")
        ax3.scatter(list(traj.position)[-1][0][0], list(traj.position)[-1][0][1], c="r")

        ax1.scatter(list(traj.position)[0][0][0], list(traj.position)[0][0][0], c="g")
        ax2.scatter(list(traj.position)[0][0][0], list(traj.position)[0][0][0], c="g")
        ax3.scatter(list(traj.position)[0][0][0], list(traj.position)[0][0][0], c="g")

    ax1.set_title("State 0", fontsize=20)
    ax2.set_title("State 1", fontsize=20)
    ax3.set_title("$s="+str(eds_pot.s)+"$", fontsize=16)
    fig.suptitle("EDS potential: s="+str(eds_pot.s))

    if(isinstance(out_path, type(None))):
        return fig
    else:
        fig.savefig(out_path, bbox_inches='tight')
        plt.close(fig)
        return out_path


def plot_2D_2State_EDS_potential_sDependency(sVal_traj_Dict:(dict, List), eds_pot, out_path:str=None, plot_trajs=False, space_range=[-180,180], point_resolution=500, positions2D=None, x_label="$\phi/[^{\circ}$]", y_label="$\psi/[^{\circ}$]", verbose=False):
    
    
    cmap = "tab20b"
    traj_color = "orange"
    ##positions
    #build positions
    if(isinstance(positions2D, type(None))):
        minX, maxX = min(space_range), max(space_range)
        minY, maxY = min(space_range), max(space_range)
        positions = np.linspace(min(space_range), max(space_range), point_resolution)
        x_positions, y_positions = np.meshgrid(positions,positions)
        positions2D = np.array([x_positions.flatten(), y_positions.flatten()]).T
    else:
        positions2D = np.array(positions2D)
        point_resolution=len(np.unique(positions2D[:,0]))
        minX, maxX = min(positions2D[:,0]), max(positions2D[:,0])
        minY, maxY = min(positions2D[:,1]), max(positions2D[:,1])   

    #V1, V2 = eds_pot.V_is
    if(verbose): print("calc tot space")
    (V1, V2) = eds_pot.V_is
    energies1 = V1.ene(positions2D)
    energies2 = V2.ene(positions2D)

    #map data
    if(verbose): print("map data")
    energies1Map = energies1.reshape([point_resolution, point_resolution])
    energies2Map = energies2.reshape([point_resolution, point_resolution])
    energyMaps = [energies1Map, energies2Map, []]

    relative_barrier = round(np.max(energies1Map)-np.min(energies1Map), 2)      
    minV,maxV = min(energies1), min(energies1)+relative_barrier
    
    if(verbose): print("plot")   
    # gridspec inside gridspec
    
    nrows = len(sVal_traj_Dict)
    ncols = 3 # 3 states in the system
    
    fig = plt.figure(figsize=(7, 21), constrained_layout=False, dpi=300)
    outer_grid = fig.add_gridspec(nrows, ncols, wspace=0.1, hspace=0.1)
    for row, s in zip(range(nrows), sVal_traj_Dict):
        if(verbose): print(s)

        #eds pot energies
        eds_pot.s = s
        energiesEds= eds_pot.ene(positions2D)
        energiesEdsMap = energiesEds.reshape([point_resolution, point_resolution])
        energyMaps[-1] = energiesEdsMap
    
        eminV,emaxV = np.min(energiesEdsMap), np.max(energiesEdsMap)
        if(verbose): print("EDS - Barrier: ", emaxV-eminV)
        
        if(plot_trajs and isinstance(sVal_traj_Dict, type(dict))):
            tmp_visit_x, tmp_visit_y =  np.array([state_positions[0] for state_positions in s_val_posDict[s].position]).T
            
        #plot landscapes
        for col in range(ncols):
            ax = fig.add_subplot(outer_grid[row,col])
            
            if(col == 2):
                eminV,emaxV = np.min(energiesEdsMap), np.max(energiesEdsMap)+relative_barrier
                surf = ax.imshow(energyMaps[col], cmap=cmap, origin='center', vmax=emaxV, vmin=eminV, extent=[minX, maxX, minY,maxY]) #interpolation="nearest", 
            else:
                surf = ax.imshow(energyMaps[col], cmap=cmap, interpolation="nearest", origin='center', vmax=maxV, vmin=minV, extent=[minX, maxX, minY,maxY])
            if(plot_trajs): ax.scatter(tmp_visit_x, tmp_visit_y, c=traj_color, alpha=0.3, s=2) #plot trajs

            ax.set_ylim([minY, maxY])
            ax.set_xlim([minX, maxX])
            ax.tick_params(labelsize=14)

            #labelling fun
            if(row == 0):
                if(col == 0):
                    ax.set_title("State 1", fontsize=20)
                elif(col == 1):
                    ax.set_title("State 2", fontsize=20)
                else:
                    ax.set_title("EDS state", fontsize=20)
            if(col==0):
                ax.set_ylabel(y_label, fontsize=18)
                ax.set_yticks([-180,0,180])
                ax.text(x=-450,y=-0,s="s="+str(s), rotation=90, verticalalignment="center", horizontalalignment="center", fontsize=14)
            else:
                ax.set_yticks([])

            if(row == nrows-1):
                ax.set_xlabel(x_label, fontsize=18)
                ax.set_xticks([minX, maxX])
                ax.set_xticklabels([minX, 0, maxX], rotation=45)

            else:
                ax.set_xticks([])


    #colorbar
    cmap = matplotlib.cm.get_cmap(cmap)
    norm = matplotlib.colors.Normalize(vmin=minV, vmax=maxV)
    cbaxes = fig.add_axes([1.0, 0.1, 0.03, 0.8]) 
    cb = matplotlib.colorbar.ColorbarBase(cbaxes, cmap=cmap,
                            norm=norm,
                            orientation='vertical',)
    cb.set_label("V/[kT]")
    
    if(isinstance(out_path, type(None))):
        return fig
    else:
        fig.savefig(out_path, bbox_inches='tight')
        plt.close(fig)
        return out_path




if __name__ == "__main__":
    pass
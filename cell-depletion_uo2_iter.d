CODE: APOLLO                                                        ;
A2OPTION: &SYST &LIMI 100                                           ;
OPTION:  'STAT' 'NON'                                               ;
OPTION:  &IMPR &PAGE 100000 130 0                                   ;
OPTION: 'ECHO' 0                                                    ;
*
*   !!!!!  YOU NEED TO KEEP THE FIRST * IN FIRST COLUMN FOR COMMENT 
*          IN THE CALCULATION IN APOLLO2  !!!!!
*
*********************************************************************
* APOLLO 2 : FUEL CELL CALCULATION AT T=0                           *
*********************************************************************
*
*====================================================================
*      FUEL CELL CALCULATION : Fuel / Cladding / Moderator
*====================================================================
*
*******************
* CHOICE FOR FUEL *
*******************
*
TYPE:FUEL:COMPO = 'OXYDE';

*Choice of FUEL DENSITY in G/CM3 
RESET:DENS:FUEL = 10.4;

*Choice of FUEL TEMPERATURE in C
 TAB:TEMP:FUEL = INITABLE: 650.;

* Choice of fuel composition : UOX MOX UTH UPUTH
* Be careful by using this two tables
*   In case of only U235 + U238: 
*     TYPE:CHAINE_THORIUM = 'NO' ; means with U238 fuel
*     TAB:V_U:U233   =   1.E-12    ; means no U233
*     TAB:V_U:U235   =  20.00      ; means 20% in U235
*     TAB:V_PU:PUTOT =   1.E-12    ; means no Pu
*   In case of only Pu + U238 : 
*     TYPE:CHAINE_THORIUM = 'NO' ; means with TU238 fuel
*     TAB:V_U:U233    =  1.E-12    ; means no U233
*     TAB:V_U:U235    =  0.25      ; means 0.25% in U235 
*     TAB:V_PU:PUTOT  = 12.00      ; means 12% in Pu
*   In case of only U233 + TH232 : 
*     TYPE:CHAINE_THORIUM = 'YES' ; means with TH232 fuel
*     TAB:V_U:U233   = 20.00        ; means 20% in U233
*     TAB:V_U:U235   =  1.E-12      ; means no U235
*     TAB:V_PU:PUTOT =  1.E-12      ; means no Pu
*   In case of only Pu + TH232 : 
*     TYPE:CHAINE_THORIUM = 'YES' ; means with TH232 fuel
*     TAB:V_U:U233    =  1.E-12     ; means no U233
*     TAB:V_U:U235    =  0.25       ; means 0.25% in U235 
*     TAB:V_PU:PUTOT  = 12.00       ; means 12% in Pu
*
*
  TYPE:CHAINE_THORIUM = 'NO';
  TAB:V_U:U233   = INITABLE: 1.E-12;
  TAB:V_U:U235   = INITABLE: 0.719;
  TAB:V_PU:PUTOT = INITABLE: 1.E-12;

* Choice of Pu composition :   PU2035 or 1GEN
 TYPE:VECT_PU   = '1GEN'     ;
*
*===============================================================================*
***********************
* CHOICE FOR CLADDING *
***********************
*
TYPE:CLADDING =  'ZIRCALLOY4'  ;
*
*Choice of CLADDING TEMPERATURE in C
 RESET:TEMP:CLADDING = 650.; 
* 1010.16 K = temperature combustible
*
*===============================================================================*
**********************
* CHOICE FOR COOLANT *
**********************
*Choice for coolant: H2O D2O

 TYPE:COOLANT   = 'D2O' ;

* Possibility to change the concentration of boron in coolant (ppm)
 TAB:BORE:COOLANT = INITABLE: 0.0;

* Choice of COOLANT TEMPERATURE in C
 TAB:TEMP:COOLANT = INITABLE: 87.87271554;

* Choice of COOLANT density g/cm3 (webbook.nist.gov)
  TAB:DENS:COOLANT = INITABLE: 1.066449039;
*
*===============================================================================*
***********************
* CHOICE FOR GEOMETRY *
***********************
*
*  ex:   TYPE:FUEL:RING     =  '1RING'  ; '1RING' OR 'NO1RING' FOR 1 or classical ring discretization
*  ex:   ....TYPE:FUEL:RING not declared= nothing=> option per default (classical ring discretization)
*
*===============================================================================*
*
  RADIUS:FUEL = 0.614;
  THICKNESS:CLADDING = 0.04;
    TAB:RADIUS:MODERATOR = INITABLE: 2.5655;
*                                                       
*===============================================================================*
*  CALCULATION OPTION : CRITICAL, NUMBER OF ENERGY MESH , DEPLETION
*=======================================================================
*Choice of the option for flux calculation
* ex:   NENERGY:GROUP = 281         ; energy mesh with 281 groups
* ex:   TYPE:CALC:B2 = 'CRITIQUE'   ; critical calculation Keff=1
* ex:   TYPE:EVOL    = 'NON'         ; NON for no depletion OUI for with depletion (keep the french word)
* ex:   TYPE:PWPG =  36.6           ; specific power for depletion w/g
* ex:   TYPE:MEDIA =  'NO'           ; NO for no saving of MEDIA YES for saving of MEDIA
* ex:   TYPE:AUTOP = 'NON' or 'OUI'  ; NON for no SELF-SHIELDING PROCEDURE
* ex:   TYPE:LIST:ISOTAUTOP = INITABLE:   'U238' 'U235' 'PU239'  ;ISOTOPE TO BE SELFSHIELDED 'U238' 'U235' 'PU239' ... MAT of cladding automaticaly done (i.e Zrnat)
* ex:   ....TYPE:AUTOP and TYPE:LIST:ISOTAUTOP not declared= nothing=> option per default (classical SELFSHIELDING)
*CALCULATION SHEME options
 NENERGY:GROUP = 281                                                  ;
 TYPE:CALC:B2  = 'CRITIQUE'                                           ;
*
 TYPE:EVOL = 'OUI'                                                    ;
 TYPE:PWPG =  19.15                                                   ;
*
 TYPE:MEDIA  =  'YES'                                                  ;   
 
*SELF-SHIELDING options : 
 TYPE:AUTOP = 'OUI'                                                 ;
 TYPE:LIST:ISOTAUTOP = INITABLE: 'U233' 'U238' 'U235' 'PU239' 'TH232';

* BURNUP TABLE DISCRETISATION-BURNUP AND STEP TO REACH BUi
  TAB:BURNUP =  INITABLE:      
       9.375 1    18.75 1    37.5 1    75. 1   112.5 1
     150.    1   325.   1   500.  1   750. 1  1000.  1
    2000.    1  4000.   1  6000.  1  8000. 1 10000.  1
   20000.    4  30000.  4 40000.  4 50000. 4 60000.  4  
   ;
* SELF-SHIELDING TABLE DISCRETISATION-TO RECOMPUTE THE SELF-SHIELDING PROCESS AT SPECIFIC BURNUP
 TAB:AUTOP:FLUX =  INITABLE:
      150.                  500.              1000.
     2000.      4000.      6000.     8000.   10000.
    20000.     30000.     40000.    50000.   60000.    
    ;
* OUTPUT TABLE DISCRETISATION-TO GIVE RELEVANT PARAMETERS (CR, KINF,...) AT SPECIFIC BURNUP
TAB:OUTPUT =  INITABLE:
                  18.75                 75.
      150.       325.       500.       750.   1000.
     2000.      4000.      6000.      8000.  10000.
    20000.     30000.     40000.     50000.  60000.   
    ;

* OUTPUT TABLE DISCRETISATION-TO GIVE FLUX IN MEDIA AND SPECTRUM AT SPECIFIC BURNUP
TAB:OUTPUT:SPECT =  INITABLE:
      150. 
    10000. 20000. 40000. 60000.    
;

*
*===============================================================================*
*  OUTPUT ADRESS
*=======================================================================

*   !!!!!  YOU NEED TO CHANGE THE RESULTS DIRECTORY NAME BEFORE STARTING 
*          THE CALCULATION IN APOLLO2  !!!!!
*
*
 output:directory:name = 'output';
*
#include <../include/data-reference.inc>
*
 ARRET:                                                               ;


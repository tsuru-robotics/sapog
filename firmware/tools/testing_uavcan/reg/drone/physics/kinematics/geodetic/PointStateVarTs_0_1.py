# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/reg/drone/physics/kinematics/geodetic/PointStateVarTs.0.1.uavcan
#
# Generated at:  2021-09-29 15:15:52.617422 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     reg.drone.physics.kinematics.geodetic.PointStateVarTs
# Version:       0.1
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_
import reg.drone.physics.kinematics.geodetic
import uavcan.time


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class PointStateVarTs_0_1(_dsdl_.CompositeObject):
    """
    Generated property settings use relaxed type signatures, accepting a large variety of
    possible representations of the value, which are automatically converted to a well-defined
    internal representation. When accessing a property, this strict well-defined internal
    representation is always returned. The implicit strictification enables more precise static
    type analysis.

    The value returned by the __repr__() method may be invariant to some of the field values,
    and its format is not guaranteed to be stable. Therefore, the returned string representation
    can be used only for displaying purposes; any kind of automation build on top of that will
    be fragile and prone to mismaintenance.
    """
    def __init__(self,
                 timestamp: _ty_.Optional[uavcan.time.SynchronizedTimestamp_1_0] = None,
                 value:     _ty_.Optional[reg.drone.physics.kinematics.geodetic.PointStateVar_0_1] = None) -> None:
        """
        reg.drone.physics.kinematics.geodetic.PointStateVarTs.0.1
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param timestamp: uavcan.time.SynchronizedTimestamp.1.0 timestamp
        :param value:     reg.drone.physics.kinematics.geodetic.PointStateVar.0.1 value
        """
        self._timestamp: uavcan.time.SynchronizedTimestamp_1_0
        self._value:     reg.drone.physics.kinematics.geodetic.PointStateVar_0_1

        if timestamp is None:
            self.timestamp = uavcan.time.SynchronizedTimestamp_1_0()
        elif isinstance(timestamp, uavcan.time.SynchronizedTimestamp_1_0):
            self.timestamp = timestamp
        else:
            raise ValueError(f'timestamp: expected uavcan.time.SynchronizedTimestamp_1_0 '
                             f'got {type(timestamp).__name__}')

        if value is None:
            self.value = reg.drone.physics.kinematics.geodetic.PointStateVar_0_1()
        elif isinstance(value, reg.drone.physics.kinematics.geodetic.PointStateVar_0_1):
            self.value = value
        else:
            raise ValueError(f'value: expected reg.drone.physics.kinematics.geodetic.PointStateVar_0_1 '
                             f'got {type(value).__name__}')

    @property
    def timestamp(self) -> uavcan.time.SynchronizedTimestamp_1_0:
        """
        uavcan.time.SynchronizedTimestamp.1.0 timestamp
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, x: uavcan.time.SynchronizedTimestamp_1_0) -> None:
        if isinstance(x, uavcan.time.SynchronizedTimestamp_1_0):
            self._timestamp = x
        else:
            raise ValueError(f'timestamp: expected uavcan.time.SynchronizedTimestamp_1_0 got {type(x).__name__}')

    @property
    def value(self) -> reg.drone.physics.kinematics.geodetic.PointStateVar_0_1:
        """
        reg.drone.physics.kinematics.geodetic.PointStateVar.0.1 value
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._value

    @value.setter
    def value(self, x: reg.drone.physics.kinematics.geodetic.PointStateVar_0_1) -> None:
        if isinstance(x, reg.drone.physics.kinematics.geodetic.PointStateVar_0_1):
            self._value = x
        else:
            raise ValueError(f'value: expected reg.drone.physics.kinematics.geodetic.PointStateVar_0_1 got {type(x).__name__}')

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: PointStateVarTs_0_1._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        _ser_.pad_to_alignment(8)
        self.timestamp._serialize_(_ser_)
        assert _ser_.current_bit_length % 8 == 0, 'Nested object alignment error'
        _ser_.pad_to_alignment(8)
        self.value._serialize_(_ser_)
        assert _ser_.current_bit_length % 8 == 0, 'Nested object alignment error'
        _ser_.pad_to_alignment(8)
        assert 536 <= (_ser_.current_bit_length - _base_offset_) <= 536, \
            'Bad serialization of reg.drone.physics.kinematics.geodetic.PointStateVarTs.0.1'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: PointStateVarTs_0_1._DeserializerTypeVar_) -> PointStateVarTs_0_1:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "timestamp"
        _des_.pad_to_alignment(8)
        _f0_ = uavcan.time.SynchronizedTimestamp_1_0._deserialize_(_des_)
        assert _des_.consumed_bit_length % 8 == 0, 'Nested object alignment error'
        # Temporary _f1_ holds the value of "value"
        _des_.pad_to_alignment(8)
        _f1_ = reg.drone.physics.kinematics.geodetic.PointStateVar_0_1._deserialize_(_des_)
        assert _des_.consumed_bit_length % 8 == 0, 'Nested object alignment error'
        self = PointStateVarTs_0_1(
            timestamp=_f0_,
            value=_f1_)
        _des_.pad_to_alignment(8)
        assert 536 <= (_des_.consumed_bit_length - _base_offset_) <= 536, \
            'Bad deserialization of reg.drone.physics.kinematics.geodetic.PointStateVarTs.0.1'
        assert isinstance(self, PointStateVarTs_0_1)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'timestamp=%s' % self.timestamp,
            'value=%s' % self.value,
        ])
        return f'reg.drone.physics.kinematics.geodetic.PointStateVarTs.0.1({_o_0_})'

    _EXTENT_BYTES_ = 67

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8D1%gC0{`ut+ix4ke#a@2k|>(GSe9+Zx2$t~Y$~yMzbw<99=c9^9Bix@wvz}A5^_n7v@4Ul%<fW_(gxspXkh~^N;E8xzV{)2'
        'LLS-6LxA?N4|ynXi~=o;z7z#oAbsm^mfs<%wdKU8K6wcRh`-_P?9A-Ud}hA$+gWyke-+yDxqsbPTL*Q!-iViNX6b4}|4gkmSiD>_'
        'n=RAU9oFwI-gT^Y&1qZg-a(7?zv!?3y8n4U)}1XIYLm|AEVdJ`Tc*L{E$zV8Yj*s;Zm_26@Zb(J>x@G2+oo<fcOBJXAE?$nyWb6!'
        '_n2ktrqS1Y-T4m?{-Uq=l$k&4|GM8jR#qLy(yMKU+5L|x$0N!*iq-GV-q2a2J}zUpTvr{n?C^qX{^3DwwtKOy?$uNy?&wVxzk6WR'
        'G%CLS8LQu;1Gb|!TYYU_TTo^cA1{d(q1?3<Tz=xHa<nYHsXO`}mE*+whOO@ytp1MSupMR{uDN67s_v8<%-C_Xz9Lg8YpU&(n^aSM'
        '?OgZNZIKYaEPkEN-QuUHYG(elf2ZGFD^nSbx@y%Y6MEFH(ybk9>NU%>S<N)+{cf;aH*5W^|M2^K_cSIM?Pir(lDRES#IhwvQyocD'
        '_n6dDZJX64TQ_P<vdt!wREx5(RO>)$(pSTgbc5o%F`amrCyL{gsA=gtbULQTS^TOSi&wBzRc*E|>9$m7+te}YQj1v|YOB@IYt%<f'
        'BQEh|YHiEn>5MMnIkjyTriPNLOtRRgZE733eA_ac<J9d@^SOyhO)40(u1YpzZlsz?>Dn#2QQg>~qt>2I_vRKwcXJQZT~Oin)JB`}'
        'QaYw&usvQ)^s(JA9}LSkI-kpLP?bmz^g5N3)l@3uo8hn|ZAj@)a{0qGOVQP;*><FKTFyxaOttK*(gRJeY5Y`+TFyC$OV^}))=hKb'
        'S}J#&`i><%Fx!nfWkfkhQrj?CjoG$p>5YS75vU_bx?_(@OVvh~QE7RL<S181Gut+g<z`Q(>upLxQYkk|nC<ISUxq{dSgKjNt=sY8'
        '&0KF#U(jnC*RO3#F~fAE8*i;k)DsM<ON;WWsTOsLc8k|nL8=}Qq&&x#deAUcw~eWxXn=^j1-~bnN^0`r?@(l0QyUH5!o0ifG}wk4'
        'eVD~I8&_15(Sczfbw=$#o#Kkay9KWUi=Q>9VI-<VJKiS{mb#(qrol0BM%-y9v<nDbRAlWn?ULf-JZV>k=*+*rscgRY;bvc3?_T~R'
        'W|`is-Tp@H#%trgVLmY8{q9`ZEl|IEUJMFszeOF64`zpkgwP$gf2s{p9xc~hpj)o-qkK5LfiRu#&LsQ1WOlV(W!)1K<6yaZFdTOI'
        'UBt9AT1MMw(|}TElquoF>itLErSi7E&+28~P-VT|-|QYQ+h*IUF*?y;<(5jrMORBW%~s+-z29~=c*!?DYZ}?~Ub2yBwX4Ktna1^Y'
        'gC{v2MD2|sUWwrVn&35(c;)~aPsNk*VJsRB%bIFawjA&>5bQsqYW~N~A<{epiD$t30}*ao#5=D>-ZKeXm5_8EnAZIbx6j)XIl8Ul'
        'W=Va)(GD?037C!cka8FDaX$1#(|0tYi0aL3(hych#=J*XO-hNzA2H6ll<iR*)7r3Gtfp`46Fr%xfcq@YN84(HTJo~!3FE<;ZrbsF'
        '?{_1As5|ev-|w<fH|++>W~<+oj!MKnXjV;X9;($_tZ8D{dyjZi9n%_5GIQmcMu7LV+uh~cYMqaMPesz+=Vv$DjRp<y-m_ZnFZwY>'
        '?%7qEs$0Vp`bwx>rTc8^2A{Ynpzia)JfFO%v+zWf8GfCwr}$w5-1>V;5Z`CHo#`oaI6jZ#A=m{R4|6-$Q;s2igxgS0S>!g@Q<e~a'
        'ncHJMWd-Mtb35BpR*}vLZdZHC8n-Jw<s`RDJ>?X)k)Cpz+i*{b;`&#R?-}HC7U`Tre&@M8+fy!Zd#0zn%IzyXMdCKvQ!a9Qx~IIx'
        '?WvyfGj31zluO*M^^~7;d!naYM!BwVd%UN_P`-6;mwU?VDCZm8F7}kGDDMXDH;!^AxLxQeNt8du?R-y3<32K|k1X!TZP!3g$>Y8X'
        's9zcPR~)vx@+R!>!Tvt%FJS)w_Ls0F*qg9huo~<>>_gZuVZVa?8ulC5Z(*OnemAtYLNf?NMIa^uvIyK1fh`fxL||V89*V%1BJh<6'
        'd@Tash`_fZ@I(Z@L!eFijmCVMDfr-xV^uzM)10#4j1}d2*T<)(k&c`Yq?zABLk}e?#Ii@CP9z<Ffuw(Us&BkNs?SaGTzBCH2?pno'
        'LZ<n-MDuf6yYi4Kx2f)sRBLl_{EMyJjL(-U6bt!cCY8y``E(|gD<tJqHkU4B)0sjhRY+ztxqP80CksikxpYp>W{bsqt|%8%g=`@&'
        'C;2t$e6k=XlcdWsav`70$;Dhw&S%nvd|ocdsX{83O=kJgOfHqp$mwjJlFw$+sZ2UA%SHN{k}0yBr7Y+_naO1exm3O==aZCMDw!+f'
        'bGcMnPA3cbbT*eQCX>ZvMlNR3ba6IWpv>f4QqEGOOr}U_^V~A&OrBz;)9GSXPUUlQQqJXy8Ok-Cp}VD9q+6HM`E)Xy%4Q36^HkUj'
        'm9~(Qlf_gqT`bCSDxFJG*^}vfO3tRzS((z!%dVhs`(%hFb=2p2H}sLE)^*kR_;A<!%~K7b{p+;$Uq<aOG)!aX`>KBonuMjQt;gF$'
        'L3}6$;vbR>x?58l0@#U_>a-PqgjSqwGLpg6g4*A=tEzVG^Zu@nYE}DRTf6>9duvmBySwue^tG)gc&jIdt)3XS`lP(pe)Wi#LwiSi'
        'cPQN6)9#G)-G`&lM-!^9M5<0Jb1|n?sBftBUp-Q~&3L3+5YjCO={Dn$ZZnW>K}fd+NVg!QTLjWA1nCxpbn`*FEke45A>HO7-GY#A'
        'Gmvg;kZ!AxZYz*(OOS36NVhPgTL{u^4$>_M>E?%Y^Fg}33h8zM((OE?+c`+Lvyg6QAl+Vpbc;f|orZKf1?hGY(rpdW?F6LTDx}+S'
        'NVgS8w`EATB}lhLNVf>2+c8MDFr?c8q+1BmZ64BX4$^HF(k%$-7Jzi~L%PjCy7?g8N|0_PNVgKCTM5#w1nE|SbSpu+l_1?pkZvVN'
        'w-TgVNl3SnkZvU*-AY2bm4tLF3F%f6(yb(<TS-W_l8|mCA>B$sx|M`<D+%dV64I?Cq+6-i)&>X&y%tg%<GIm!OXmx~8u#-!4;UMI'
        'z8WSG=(+|Zo2gQR?XiXwyLI>7b$6A>qinlTT3q~ap9nvs8V)lIH7?!eZdHAcjvy!QA=(@Iswffey<mJiiE00?{fqXW+LPT~KCt{('
        'do-|E|DS<{&Lv#kmVj<cjCET==(dEb+h~MI9U5c0fBP#$kX+|5>D@OaAttU$qlxXRTM^>^hF(I`;(i)hb=Ndnog3V1M48sKVdd=8'
        '2{#5`?4!mu-+oJYkaz+%E%x1X8|ne~sJXG|GFy13dE)HTHdQ>O%@eq;S`M>ma^<CE?y^7L|GrW3&cw?2<aN{FJ{9AcOYH8#aD{C#'
        'gL|i+pW5y|HKO}v_m3%bRQzX*(KFLAdOAi=$7nuAKZOUgIU5~fqw^d#ysoE!$Mxht!u1pa8}lC5(=o8&2OA*|8w(!S(-PPSfek;{'
        'SOpu49@kR<Y(&Av8rWC?8xgP(0vkaO8|T5s8L)BM<9a#{HkQD~F|ZK=8?#`;4>n#08!@nP8Ejkv8?S*432a;d8|T2r8L$xr8>hg='
        '8rWC`8!KRA32a2bMi^{_z{VWd2!aj2hYjI+ih+$N*a(4*4%p~`jSkr8fQ=5==zxt5*ysp0I)aUkV51}0=m<7Cf{l(~qa)bp2sS!`'
        'jgDZWBiQH&Hadchj$orB*ysp0I-Cum=BG4FY52+0uscg4YdAX$h=;**c<_06@Ph{*cnElS2!IDac$ftbKJX9*4`J{S@$euXOhmwg'
        'A3Q|BLjXLifQJxx@PUWp;2{hi0^lJE9#+9a1U$@ncsT2MFmW6_M8Ly5c<_UVOW;8Q59h!`6g;efhZXP;0S_VY5CjiC@UQ_MUI!0X'
        'z{4f*a1lIQ01s!uLlium1P`m=VHrF`z{3J~m;(<14-ZN3umT>oz{5??gNYb;h=PX@co=|(0eBdIhk@W>Ab1!E9tMJkf#6{vco+yC'
        '27-ry;9($m7ziE)f`@_NVIX)I2p$H4hk@W>FgZI+X_(URlcxc`p4s8fjiC>BVtd!wBet1YmU__duHE2!D~6Blukk~N_jWCoS%dKn'
        'QP^}gcEPVqxZu09`CKlUg+G~l64aJj)18C9GWTo`#qI9u9oAxw{_Lmy{_=f(>0uATO3%I1ic%r!D=$F(jEDMJ5A}1Nhw~v1^|PQp'
        '0_x{H)E@)&bD)04^Kd=_>O-JD=%M~3s9y#3%b-32>K8!$9H<X?sJ{T}&w=_gpgs!fPl5V1P`~PVIKKqyBcMJE>O-J@4%7!hz28H9'
        '0@TMr{RXJN3hLhg^{<2abx<Dz^;basWl;ZfP=5*3{|wZ>2I?<@dI{7=L463+S3rFQ)K@@#1=LqSeFfB4Kz#+&S3rG5P+t+$R|NGH'
        'L48F~UlG(-1oag`eML}T5!6=%^%X&VMNnT6)K>)c6+wMPP+u8Szf?2#RN~sGv2xpT2>-2R5{n<X4|G0Be;j_l#rG##`i|yE4v)Cg'
        'V8SOkzLtA0Eq#CJn-t#A$@3HY9WBP4q}<1AN~+{gir8@1YN!VH{90yvXXpvV<|0-f`Bf7mw`x56_Hbw!xk``nz6#H)^p5jex?D$I'
        '=-usr&!_$K?r+HK?$F2B58eKe{Lmk$)>E$N?|<C&g09!yPq~*}xLc<(X)2R`@-k`nK>&;BThffC@{b=*M8HFY_W^{@<5u!}i12$J'
        'Km<HQtbhm~hzNMxO3NU^4<aHSA{Ie}A4IHr9zclweXAg1!9zq8M67^_5Qy-Bi1Q%g6o^>%xRqu=#3c}M0YpSW#43o0fQUH{5pRHq'
        '%OK(+h&Tr#PJ@V55V7ca01@!)@5_RSB#5{QB4Qxol1D=LKtvQo+y)Uz5U~Ox9)gH{5TSvHEf8_jv%fDUh=>XzLLh?rACPcEH%FnZ'
        'QAitw_D7+IqtKV5&{w0-*Q3xkqtLgb(34T<I}sZ4;f6-5>M0&mJf?U&g@@QuA=L3xEA5GGZqI*-%zY=MF??C*1J*G4N;xyJS=Imi'
        '&8n|@_R#Gi2}-L*tLV&gw$Sa~4?sM|b`7qC$Lo1%ay@?~lTD`ObS9h6XXIR3mUBfp#kbL=<V;r1@=a~&TsE7;ihtLkw3NUzHSF$Z'
        '<19ZPMmxN$m!`}5>9T&htUtW0Uvby(Wm>wI@$%#3-poIrrPb?s`WSD|+<uAMGsS?Cz<~1NyEAuVv+nXUGzEJK_7v>O_j>7{Gch0S'
        'Xdh0yb3bg_oqE%!bWZ7fVQ+f(+D9>WE=~;R;q_0_A4@OhQy)8@|C`U-C;11PqmTcYo%BEd$?wenJh9$LOs+R*R!<+^5&h}Abd_pJ'
        'LIDilK_1^yJp5jjzwpe&TjcuiM*&9Lmeq!2x2x_e$y6UlEmS66`slxG$M;{(PB^}&W7~9W`^k@OyS};U?y>2Epy`94>F%*94O1GP'
        'y?ZPq#2J>RP^=NIrv7R7i+Pf(i-+XuXFt+*3Gw?7Prtr*_AX=6IF9>kH*}$@H|&=$EB`Gpc4$o>kWC+uO&^dw^?+=*A#~=g#~hHy'
        'F9L|q14!_Qxz*=+Z^!3(!!rm#d>%l8p1E}vfcOB&s^`6(H4h-Oo;N&C0+1j8SpgtE0J7`>WEFq}0mv(!x%CnNi2{%a0Pz8k^8jQO'
        'fXsW|+qnQh)&NM@1IQHsashyx^t|CIen2S+Kw<zy0w7TUvI0Ot0K^ACasVU_K(2TINqXMf5pQ_<0LV=M5(OYV0MY^=w*g2JfUE$J'
        'CjyXf1t8yux%F!?w|*t&)-T1}`cTZR`(kd@#N4_i=GL1}{eV(T%&k!|w}u21k4I2E9zpT=(58wh5>q4u5|bU|S<eOViwS?H9pC+%'
        '5b2J8_%XbM&z4>H?BD%nRqgI*NhZ^hOy-PegH4)I{(4@_C{aJ*Lm%SQh%4_2UZ3&*1MCLX>=Rf300'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

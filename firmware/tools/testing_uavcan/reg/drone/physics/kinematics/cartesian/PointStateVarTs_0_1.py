# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/reg/drone/physics/kinematics/cartesian/PointStateVarTs.0.1.uavcan
#
# Generated at:  2021-09-29 15:15:52.571780 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     reg.drone.physics.kinematics.cartesian.PointStateVarTs
# Version:       0.1
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_
import reg.drone.physics.kinematics.cartesian
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
                 value:     _ty_.Optional[reg.drone.physics.kinematics.cartesian.PointStateVar_0_1] = None) -> None:
        """
        reg.drone.physics.kinematics.cartesian.PointStateVarTs.0.1
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param timestamp: uavcan.time.SynchronizedTimestamp.1.0 timestamp
        :param value:     reg.drone.physics.kinematics.cartesian.PointStateVar.0.1 value
        """
        self._timestamp: uavcan.time.SynchronizedTimestamp_1_0
        self._value:     reg.drone.physics.kinematics.cartesian.PointStateVar_0_1

        if timestamp is None:
            self.timestamp = uavcan.time.SynchronizedTimestamp_1_0()
        elif isinstance(timestamp, uavcan.time.SynchronizedTimestamp_1_0):
            self.timestamp = timestamp
        else:
            raise ValueError(f'timestamp: expected uavcan.time.SynchronizedTimestamp_1_0 '
                             f'got {type(timestamp).__name__}')

        if value is None:
            self.value = reg.drone.physics.kinematics.cartesian.PointStateVar_0_1()
        elif isinstance(value, reg.drone.physics.kinematics.cartesian.PointStateVar_0_1):
            self.value = value
        else:
            raise ValueError(f'value: expected reg.drone.physics.kinematics.cartesian.PointStateVar_0_1 '
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
    def value(self) -> reg.drone.physics.kinematics.cartesian.PointStateVar_0_1:
        """
        reg.drone.physics.kinematics.cartesian.PointStateVar.0.1 value
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._value

    @value.setter
    def value(self, x: reg.drone.physics.kinematics.cartesian.PointStateVar_0_1) -> None:
        if isinstance(x, reg.drone.physics.kinematics.cartesian.PointStateVar_0_1):
            self._value = x
        else:
            raise ValueError(f'value: expected reg.drone.physics.kinematics.cartesian.PointStateVar_0_1 got {type(x).__name__}')

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
            'Bad serialization of reg.drone.physics.kinematics.cartesian.PointStateVarTs.0.1'

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
        _f1_ = reg.drone.physics.kinematics.cartesian.PointStateVar_0_1._deserialize_(_des_)
        assert _des_.consumed_bit_length % 8 == 0, 'Nested object alignment error'
        self = PointStateVarTs_0_1(
            timestamp=_f0_,
            value=_f1_)
        _des_.pad_to_alignment(8)
        assert 536 <= (_des_.consumed_bit_length - _base_offset_) <= 536, \
            'Bad deserialization of reg.drone.physics.kinematics.cartesian.PointStateVarTs.0.1'
        assert isinstance(self, PointStateVarTs_0_1)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'timestamp=%s' % self.timestamp,
            'value=%s' % self.value,
        ])
        return f'reg.drone.physics.kinematics.cartesian.PointStateVarTs.0.1({_o_0_})'

    _EXTENT_BYTES_ = 67

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8D1%gC0{`usON<*wddGXnd2mLQG#WijTe95pYBiLtA)C!6*>vK>igp!k+8ztm!$O>0vPqVvdqlFi-ObUA69ZY~0SO=w0^0$6'
        '%V_~00^}GSiEI!U$O6eB2OV<IAqOFg067GR5g<UmYW|Dlv^0LLV+2SKF#L+$)m7Ei_51!`RW<)`{?GsTcck!d@Jes5<+a+mn#Ww*'
        'Y}+52jW)~Gnog(Zc(%`i!QmUe+i&`Pm)+d!vEZk{#h(Np1=+zut!sAZeA#7Nxt8m6S*~a8d3Mvw-Lt!_WBNSVG+m#0w%N^HckHfz'
        '!#90)+jMVw!5~%JVXkL8-N2FtOSh5!X<$gk+@A(N2?mF1rtiCUqfaFSKcp%TXzV0cFj%;1vvzCR$dy{l^v#;jTW%%B2d#y{xxTs6'
        'q&E3>hvjbUb(<Eo-~N!bZqfnIH#@z+TC$dnIYZ(tvC>q#wTjD+AJmSXYj<ql-l29Jzt#2ZtuAZ*pzE_O=I-yhL$!wO*V?SR<y(QF'
        'Q!AUM=hr$;i&}YRaO%1!h+mewLg(J$r>JY@{v>!W7@Vk48@nyjZOs<+u-~9tJJhk8uH&($(`^NV`C7|q26z57AxSqaCU^Ut26JWS'
        't~`^=lYPtdWy{=Qa?kWU){;HD+hnrmbeL?qRE2B0dvb@qc756IQvNWfpIhOD;y4xRxb_yE&e}PayA<Z)9V|CYk6n~)Pj0chG%{Lp'
        'kGUIWuh+JlG)SCoPUgil`>xB&nOwqa>U(U39+cc*vdezlr)NW#-*uhNv~+Ls_`<^E4mFIqmt>EzFjLc^a=jkisNLP7qwbDP_ZBwA'
        '4r^bbyP(GHnC(8}t@Ita%XWA-(Z}7kbAQ~v$@x-wgSte%Z?~wOtZ7mk-&k3Z<qcW=QK`JYXDPecaQeQis(MM@W2Wm}lJ8q~)8eOk'
        '^yK`#oP1d>Yhjr)*HXLtG<ID1zSD2Fs3NLCmiyf<YckI>UAw(EZUPMi+4j9jYpL7lGHNY<A|<NTx17GmbA{E@=~kbLkWH$M3TC@D'
        '^;g%YaV$4o+q1pg_-3xOX)M^yjVqTo<!smS<*VPjDAP#jQeV1MACXOiqTl2FRgoKe1SzkvXYREfGknJMpvXhy!iL`zk4o<F=5JAE'
        '&obL>{)G8(+iJ6oF#EWQyKLG~9YzPnW7MBK2O1RXJ|7mm4_tn>OAkh-PV{mCfpBDyy5e*>CjNvw>$r6msdI*Iy=t8|B+iqyK1OHh'
        ')~2!f?)#g8b#ZXvcbV%%s}9E-JvZJP_qxvgZY~%s*1`q_gO`O<V7omUaNL>ga|x;U!trUgMSHB$V3}^Y$&Ye(cok_nKbTVj-ZHPz'
        'Z?M7f89!KS?2Y{{zl*H(l2x=e`s7erj4CCZSSxrqI8wW7@3K~nKd74B3N{DFYM#?~n~YAhS*>T1yBJt`zthX_nfLns25<Sshn=pb'
        '?kMeiuiqdxYvkDbZC>QmiFzAjyz*lQn&&-|f35?~6>>^$oQvFH%`!czmIGb`g26-T=D*(@Bh4$2c?Ent5aEtXyz_44Ba^T-2}%FH'
        '<KEi{$GkUFWB63UDrqeE);@-)0H@s_QyxM-t%tr?_LfByQNKAIa$zl0%tvIyp_0h|2tONAwnKRwcf;$krhV6*8ObC8_gId5+eVw7'
        '<OMMjrp}pe+K+w@2I=3j{kOyKH`rvD4w5ye7YyWs3i0+j4Tl~N_3AsU<G}5`OT3xB<4#3pvDUN*@W8r0IC|Y|aqss`ChHbIyV-BI'
        '$-zg@TBSb=vW7nN8YI=daS4Hu>Nn^<J9d`~7bVPHo>=1IMT3PGYRvKLq@j_3O>&zU8uR$R!0p`7Sj6!q98bY6<M;}<i$miO@~62?'
        '4UNOx&JT?v$bXdELqlT~=Z|r_Ff`Us&T($nhQ<kQSBJ()ZjTI&Q{1M9#tYo842=w~e-ZV*gnCY+oHMBJWo}OojkDaoG&Ek}_Qjzg'
        'bDJ3&=eT`gXuQhpsiE;5Zch%4^W2^o8sFvi_|Uk3cCB-JY-nWBzKh%*9U8Bpov(9ycxYTgdpB^uIkY>^?efr2(Eb9qOG87&eH76j'
        '8tx~2uF0WM#(h=LzdG)(I)3iP8?e6y`|Gf8!u|&AZ^FI>dkyvutOdIZ`vCT1*iT>|!F~$+81^abXJh+LY7U8vNMuDq7l~^kaYrO9'
        'k=PZ92O{yYNPHp^k3`~Ak$5Z;PetN0B>EJ;k<TZk;LaPz8r*f0rY!r@i1Ok<;?gvUBWD6q?dt^5;}{juawJBbDLemF%Kq}jUivD<'
        'K2zp%ixgqGXXpA9oaM%DFZVvV{M)QauBrG;SUwY#pFUuA;JW4>#mrZ^B#yo9WqxRXNPf7++Kk7sm@AwaEMKKK#^0BV!iKjfY*4NB'
        '2lUK4<`y-w&tvvC@08{wsZgm_%GF|_sOe?3SSVE#y`YuUil!DT#X?2ViluU;sw)+RY)LKYnpUlrOI5vEsA!e4uJCKrvQp6%g~G+6'
        'UMVXjy;>^i<)T_Cm-UKXs1!<?qVc1}Qb8-~s#d1rwW3-ms%2fT($|7cnRSh-pns)UDppE`a#b%YR9itQRm!DOLDf~IQdYH+R#lX$'
        'Qq-$Ol`htl3RR|;6kVfC#bTAp=Cu{oVwrNOs#?|bLb;?XdZ|<`Qmtx{?v`$mZe3T)s-hJ%twJ|XjV)4ZD+OJt7OHBss_O-{q)^)x'
        'wOr7(f~x6MZdniG9MY6!ngjLBrtR+qM$-C$_4ZhU-nHJFk*c-#SdaPk^93(ayT>oRWqmLsUvCXV5bMUsGU>l@pgu_veM&%|B<NEz'
        'qEAWaQv&+50DY36Pb<);73fnM`Xoj4DGhx}K%dgkrzG@g75bEdK1tB0W6-A+=u;B<lz~32L7&plr$y+K1bsRk(Whh3r!@3w3Hp?P'
        'KAnd?$<U`W(5DRa=>+s?75bEhKBb^f^Ux;=`m_OkdJX!t4t+WgeL4qyItzU|4SmW$pH4!b)}T*Ep-*Y((=zmF5&D#bK1t9g1^ToK'
        'eYyjEx)#x=Ec7V@eM&)}M$o4b^l1cr8VP+G34Iy~eHsaU8VP+G34Iy~eHsaU8VP+G34Iy~eHsaU8VP+G34Iy~eHsaU8V&o_2niud'
        '3mrx=JPDHZ^M1p$E`Jnk*T{ca|KeF!9$Meqw7&n1Ob$Fd&)s-_?8fsmZhUrfVEy((-jL@b|NbQPpH_{>o-xTW$uY@OlE;e=vn2l='
        'C;6YJBzwOK$#gCs#&~(ec=>6Jm!HIV`7p*Kqzn6?9=vu%<dB<=<I)7u#43>~_xL5@6q{6^CeL5M|8|StR_p>|7ZAIE&v5}W)2gRP'
        '{nGlk$?Rnnvlr{%tv3e?G!alV#NXC`7>mzG@V}7yZ_2Pgwq6ynb)9gme+3-pA~-HYa9oV6{iGr|E&#_ga9oVwcnCNy0>`<?+D{rd'
        'rhwyo1jm!WaSb>g1&(RpxC|T@fnzd)<5}Q%1~|S195cZ26mUEN9M>XiKSzLL8aS>1#}sf}1dj8-F%iKr4;*vAaRWGB0*<c($Jc=4'
        'Mc|kPj_bhj0&x5;a6AtjzXKd!1&-%{qYNA~z%d0J>%g%N9P7Zb4jk*iu?`&Tz_AV->%g%taI6a)>jKBRz_BiHtP33L0>`?*u`Y0|'
        '3moeL$GX6=E^w?19P0wdy1=n6aI8;pJkoS_OqV3D$!dMq=c_)|55jo+N9qq{`Bsl_e!2FR<;y<Lw$)}_5XU=J;!2qm*0p!}P6p$m'
        'p54wRNdEq5`!C3B=jo$A(f6HiOW$vs?lThq#c})W^!?-&r_1*!y3bv*=1Ty4#oA?EzT5lUDBu_4C}1v*0^%qjjskcTu>A&k1LhGA'
        '@5pnO$v?h45y=P<a}gpW5Rn2Ai3kx15Rn2A$p{gvAVLBWNf40&5l2Bp0z{-EL>vYY2@tUcB2tk}m^Bcw93dhDB33~}3PeaC;$;wV'
        '3Pc<Q5h)Nc2O`dch_fIf10vQyL>fdaMu>PFL|gz7=Rm|65b*+tSOXD<K|~5fBqN(J8i-Ip#3c}s1rg^XLM(xZ42ZZ6A`}p@3L+kW'
        'h+Pn2frvXG;#y=ACM$@@2qID-g2o?^2vgT4sXLRDHA(GGQV%Ank0+^5CaFi0)Tfiw<4Nl2B=wm{jrj;u4KZnq@rdz=@puLggsrLY'
        'b-(asyy!%7x<6O?+%3QG#hv!}jjr3Q?eM*v;>><x;`8?tUx{q~?VyO<7jOMNcdjeX&UM#|nxg7zQ7e~=dP&vwQdKYTExCeT)O3w+'
        'kf|k2Q>L@w<QL6`qdQG<JR6Q@!|`l*|7>_QocY#hrdPu&sk2Mf*XL<A`y?qz)79#`-{8KJ@F4lGz3a67%jC?ea}0J2b_{mB>Kx-3'
        '<M@An)%o%V*-(7*W8uBXm!H4x>hoW7p?*wSxSd^~k4N*f3($Y?zqSB9Go#4Q&L~L6)%`ooKYp98GF@3n{`gh!=`H0}-fi&r&Y5_b'
        '-yZ)qL-z3FCbKPj{YLm^IQ7RtQ;{1@vrX0WI3oDc3*Xy+nUJLL%l2PU>Y%0VTk|tZ+p%wpecS(g-?shpc`R+mTRrhsPrTI=zy1`{'
        '5YrHO{V64aGt5O1vHk;JxcSBQ?L`V#|1mimuKxbF^}dAona;ECMV`LFm^{rB{_3#BeA8}w-+Wy8v&3`>E8YW(_rT&kuxIwbw(|?('
        '9f~I$kSAXS5Gex4`~l)B0g$B#AZY+H4?v^{AoCG%T>u~w09gYdYXIa#1ds&)k_I3r0mwW6Sp^^x067`~WDS7K1CSRZ;(8u{WB^DS'
        'fJgx3WdO1UK$ZYV7J!@uASVFGN(7K~0CE<9oCF~0$PZZ+0FnhDG62Z{kW~PZ0w59qDFKii09lU!BE&TdK;8l%5&*ddKr#Si2taxO'
        '<T?OR0LUr;c`5*TECBgbi0dOEuAc~T{aA?W10k-vLR>8&u6KmEUVG+;tXUzh86mDI0mYLE6i+5lJlXf&M2tj?M2y7T0ec_gc+>hD'
        '>)7@mEm5TPx6?@Tqi;LXyy^WaFX(=`c+$EtnTF~#4b{0@utu9CqQAE&L^P8ik3k>e)WnrUPw)=S{SWwJ3#*Sx000'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

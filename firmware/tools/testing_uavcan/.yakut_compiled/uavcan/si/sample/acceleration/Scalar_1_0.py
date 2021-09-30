# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /home/silver/zubax/sapog/firmware/tools/testing_uavcan/public_regulated_data_types/uavcan/si/sample/acceleration/Scalar.1.0.uavcan
#
# Generated at:  2021-09-29 15:16:17.605477 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.si.sample.acceleration.Scalar
# Version:       1.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_
import uavcan.time


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class Scalar_1_0(_dsdl_.CompositeObject):
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
                 timestamp:                   _ty_.Optional[uavcan.time.SynchronizedTimestamp_1_0] = None,
                 meter_per_second_per_second: _ty_.Optional[_ty_.Union[int, float, _np_.float32]] = None) -> None:
        """
        uavcan.si.sample.acceleration.Scalar.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param timestamp:                   uavcan.time.SynchronizedTimestamp.1.0 timestamp
        :param meter_per_second_per_second: saturated float32 meter_per_second_per_second
        """
        self._timestamp:                   uavcan.time.SynchronizedTimestamp_1_0
        self._meter_per_second_per_second: float

        if timestamp is None:
            self.timestamp = uavcan.time.SynchronizedTimestamp_1_0()
        elif isinstance(timestamp, uavcan.time.SynchronizedTimestamp_1_0):
            self.timestamp = timestamp
        else:
            raise ValueError(f'timestamp: expected uavcan.time.SynchronizedTimestamp_1_0 '
                             f'got {type(timestamp).__name__}')

        self.meter_per_second_per_second = meter_per_second_per_second if meter_per_second_per_second is not None else 0.0

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
    def meter_per_second_per_second(self) -> float:
        """
        saturated float32 meter_per_second_per_second
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._meter_per_second_per_second

    @meter_per_second_per_second.setter
    def meter_per_second_per_second(self, x: _ty_.Union[int, float, _np_.float32]) -> None:
        """Raises ValueError if the value is finite and outside of the permitted range, regardless of the cast mode."""
        x = float(x)
        in_range = -340282346638528859811704183484516925440.0 <= x <= 340282346638528859811704183484516925440.0
        if in_range or not _np_.isfinite(x):
            self._meter_per_second_per_second = x
        else:
            raise ValueError(f'meter_per_second_per_second: value {x} is not in [-340282346638528859811704183484516925440, 340282346638528859811704183484516925440]')

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Scalar_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        _ser_.pad_to_alignment(8)
        self.timestamp._serialize_(_ser_)
        assert _ser_.current_bit_length % 8 == 0, 'Nested object alignment error'
        if _np_.isfinite(self.meter_per_second_per_second):
            if self.meter_per_second_per_second > 340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(340282346638528859811704183484516925440.0)
            elif self.meter_per_second_per_second < -340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(-340282346638528859811704183484516925440.0)
            else:
                _ser_.add_aligned_f32(self.meter_per_second_per_second)
        else:
            _ser_.add_aligned_f32(self.meter_per_second_per_second)
        _ser_.pad_to_alignment(8)
        assert 88 <= (_ser_.current_bit_length - _base_offset_) <= 88, \
            'Bad serialization of uavcan.si.sample.acceleration.Scalar.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Scalar_1_0._DeserializerTypeVar_) -> Scalar_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "timestamp"
        _des_.pad_to_alignment(8)
        _f0_ = uavcan.time.SynchronizedTimestamp_1_0._deserialize_(_des_)
        assert _des_.consumed_bit_length % 8 == 0, 'Nested object alignment error'
        # Temporary _f1_ holds the value of "meter_per_second_per_second"
        _f1_ = _des_.fetch_aligned_f32()
        self = Scalar_1_0(
            timestamp=_f0_,
            meter_per_second_per_second=_f1_)
        _des_.pad_to_alignment(8)
        assert 88 <= (_des_.consumed_bit_length - _base_offset_) <= 88, \
            'Bad deserialization of uavcan.si.sample.acceleration.Scalar.1.0'
        assert isinstance(self, Scalar_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'timestamp=%s' % self.timestamp,
            'meter_per_second_per_second=%s' % self.meter_per_second_per_second,
        ])
        return f'uavcan.si.sample.acceleration.Scalar.1.0({_o_0_})'

    _EXTENT_BYTES_ = 11

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8L4#Cb0{^vFTW=h<6_#wvy7?N}j$`LSr>-Tn-dSn2E3eb0t*g{cz*sgcyAfKnQ_c*vBs{m097$`SXj7nt1q{#uG6nJz@)Pn{'
        'Bz*`_pwIaUL4QFWd(I4JwQ}so8j!y;<l#Ao=gR%_iGQfm6V<=`t#laZAaq>Km1LoO%Dj*}uAf9{qNU+wetOHO%r}|hkA^8PKPi_#'
        'F8^3A<x_6VBG|v4v0b0Vj+TyQQ3|J-@AHr=W@HjOTRsb!D)Sk4mn#h`rI^U4e`V=UN;*j={#Jfm=JPHyMoBL-T$jHE1urpe#8u`~'
        'cO?&lLzCv*fEnf*v{M|b7sXV5&01(=#GS2S><g8|@+l7<!GbnmbSb9AY-5Qy1=__qdwk(#cBD#1(#Tz~W8rbE<sjz42eIJ;u8ult'
        '-u0w$Lmm%|C}|(8^qDqplmuYq>-nVzjUYVcY{1?<+(Os<wR~9S7hJG04wwqY1s!A_Tx~v*zDhLrlQ<~z6K;_B<@SG%O-wuzoWxn='
        'aYd3HGRCEe5zG+5b~#Cz);u6u#y%%Hi8x^jR4Ar~B!bV_5E%o1#c7;56l&K&Xrkl*wwI*CotqUGI+%D&^JOA63HXi#pOBQR7E9Am'
        '`gKMS6ys+~p`6hX)RbvH2Z16UCyM_egV@0F9hF3f()B2Ol`s;4VO-rLn)8auPe86t;i57gz^dAnaJR}7S!thxTYz!9EX+7sX%Z6i'
        'U33%tw-Y9NwSA-g-g*mMLiS_;c5<JAjql9O5z-=^-}TmydKTE3mt=-?I{h9Qa;Ef6vL~c3a0^N!HbaNpA?w{r=Ga-VJA>R&WG~6W'
        '02F}+Lb5pKKG&Kl84ha`AQ6Z(dSorQ4UU1e7?B=mH6qD0a#iYKJIFu;VW15J^L+{aiVfs3@s-q4JN0EYLdXT_w>Iu<lBGB?<nDXR'
        '1TrB8Un<b&GX+VJrRc9)#2Z49qQ;aB!-Q2ahCo3-a4N$eHK8IAnm+($Em#<0gfZO)A#YXewTc~n=%|RpLY<>#6bDF(MT2R9K2W$D'
        'LtqFvQ9C6R!kK(#BZ;w0%&6|ff_T$X*Jxk7Ew0lEtS7Npm(KL#O}csiqs>w*=Qn=MRr0**D&HV(=#3|FvKKpLe$uTBD)Tp*roi`8'
        'NH}a}M_R(n!zw>n*w`a_`7B)7$5jpccP$P3`Q%E8mT52Zc)l>!2VHMicUio}lDHz)L@R@a5^zuo<-~*XAV1^o$bBBT7${c;<z{}~'
        ')k&s&4jUnNQwHrK|5IB)<+im9A#>VKGmq`JHA|C0dq=8hk15_ZNfPQds5KBFw{Dv4H1nWxUBw4khzbu|tZrKtbX5C=ebrfYR-Bp('
        'x}+<Z25YeHU0a#u0eJu4n{}n5WP*}0O`z}-1#JMmiwO(W%%D=uUZS3~s#4Hn8mnMcDj`LTI8s_5APKX&_^aAK)B_(v4g?ezxHE~M'
        'vjtW$CaRZ!Bxp-b`>l#^7kCoY(kb`ljvPyHm<&(2gH6~AA;3491Uc;4aB1`WcbT91xilYE-&=f?z4>uBNz0tPOo$#vUIK9euioQP'
        'V!Pq}6sK;Y4rk9v*B4OtrFf8^eZT^2ir--pk8yW13t>(VpWhX|zn4q2UuX{|cv?#+=}hLqJtG<8JOhI5BQcFL4YCA<(n&lwQP5)+'
        'k0Tx{=n4Bhg*aKzlXiXDuFqJUwd-?;Ckr}n`A;Fv6!bLWiGrT7{AUs83wqA(pGTZ3=qpyv0^%zLy?}VGpcfI(6!a3}se-<WI9Jfi'
        '_WWyB?-i@(s+IG))%OPC)q=i>c%`6kA-+~nf_S;0*AQPV=-Y^w3i>_7iv_)oc%h)*M_efA4QtmT;`xFuS^Jg|&ldCt*3KUyo-XK3'
        'Yj4Zm*RgiD5oZg!V(ni=oGxg`-eb-BqigR|#r1eW*X_M-S^xI!{chKBr|($&k;NZdeAnVnEdJEu&n&)gaoeJ>xNq^9#ZN7MX7O{2'
        'Us?Rx;x`t*t?}N>q$Msl#8N}_8{++j*lq~X5c>`BtRX&ah|e10^M?4UA--;iZyMrTOJwk@gHZqj1bez&^RT1CsF^i~56$I#0w>n!'
        'c?mDT*}E`9&5=hVj4T2pt0NYlf#8S@;PsN>d-2_Tajm=3>37z;>+5U%UZ>yh-R`fh-dgFd_Sd@oZf|w{cBj|v)+41-e>LLpMsT6B'
        '-MS@?kzkPc62^|WgId23=f!`-zcR6LAl};)zsUdc|C<_Gw(H*u?eX6W?fUn^_}~z~JU}DG2jauJCEXVfN1f}V5%qAan_Yz00FKA_'
        'g>5mPt-B%&BK)E8LTOvVrIX;j-^0^^!Jh|u|G5bZzZq+b1ll6k$g~Yi+lNdpcF6B6V>USd1NZlSr+p0o00'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /home/silver/zubax/sapog/firmware/tools/testing_uavcan/public_regulated_data_types/uavcan/si/sample/frequency/Scalar.1.0.uavcan
#
# Generated at:  2021-09-29 15:16:17.620895 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.si.sample.frequency.Scalar
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
                 timestamp: _ty_.Optional[uavcan.time.SynchronizedTimestamp_1_0] = None,
                 hertz:     _ty_.Optional[_ty_.Union[int, float, _np_.float32]] = None) -> None:
        """
        uavcan.si.sample.frequency.Scalar.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param timestamp: uavcan.time.SynchronizedTimestamp.1.0 timestamp
        :param hertz:     saturated float32 hertz
        """
        self._timestamp: uavcan.time.SynchronizedTimestamp_1_0
        self._hertz:     float

        if timestamp is None:
            self.timestamp = uavcan.time.SynchronizedTimestamp_1_0()
        elif isinstance(timestamp, uavcan.time.SynchronizedTimestamp_1_0):
            self.timestamp = timestamp
        else:
            raise ValueError(f'timestamp: expected uavcan.time.SynchronizedTimestamp_1_0 '
                             f'got {type(timestamp).__name__}')

        self.hertz = hertz if hertz is not None else 0.0

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
    def hertz(self) -> float:
        """
        saturated float32 hertz
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._hertz

    @hertz.setter
    def hertz(self, x: _ty_.Union[int, float, _np_.float32]) -> None:
        """Raises ValueError if the value is finite and outside of the permitted range, regardless of the cast mode."""
        x = float(x)
        in_range = -340282346638528859811704183484516925440.0 <= x <= 340282346638528859811704183484516925440.0
        if in_range or not _np_.isfinite(x):
            self._hertz = x
        else:
            raise ValueError(f'hertz: value {x} is not in [-340282346638528859811704183484516925440, 340282346638528859811704183484516925440]')

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Scalar_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        _ser_.pad_to_alignment(8)
        self.timestamp._serialize_(_ser_)
        assert _ser_.current_bit_length % 8 == 0, 'Nested object alignment error'
        if _np_.isfinite(self.hertz):
            if self.hertz > 340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(340282346638528859811704183484516925440.0)
            elif self.hertz < -340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(-340282346638528859811704183484516925440.0)
            else:
                _ser_.add_aligned_f32(self.hertz)
        else:
            _ser_.add_aligned_f32(self.hertz)
        _ser_.pad_to_alignment(8)
        assert 88 <= (_ser_.current_bit_length - _base_offset_) <= 88, \
            'Bad serialization of uavcan.si.sample.frequency.Scalar.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Scalar_1_0._DeserializerTypeVar_) -> Scalar_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "timestamp"
        _des_.pad_to_alignment(8)
        _f0_ = uavcan.time.SynchronizedTimestamp_1_0._deserialize_(_des_)
        assert _des_.consumed_bit_length % 8 == 0, 'Nested object alignment error'
        # Temporary _f1_ holds the value of "hertz"
        _f1_ = _des_.fetch_aligned_f32()
        self = Scalar_1_0(
            timestamp=_f0_,
            hertz=_f1_)
        _des_.pad_to_alignment(8)
        assert 88 <= (_des_.consumed_bit_length - _base_offset_) <= 88, \
            'Bad deserialization of uavcan.si.sample.frequency.Scalar.1.0'
        assert isinstance(self, Scalar_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'timestamp=%s' % self.timestamp,
            'hertz=%s' % self.hertz,
        ])
        return f'uavcan.si.sample.frequency.Scalar.1.0({_o_0_})'

    _EXTENT_BYTES_ = 11

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8L4#Cb0{^vFTW{UQ5teMry7?N}j^o_cxmZ$b@#uEs<Fsk(Ds>ZVEE|@c2rXK6Nv_T=Omf-XrKDq^X!Fp*0tl2qSRg+kKOv7r'
        '(uV*A`kbE-^cUnYGvx9}a_q+#kiX&X?9A+3_x$a|zdkxWQvWMn&jyi+V$U~ROBTz=EQq=1hbqaGk(O7*=}oKi(B_&y7-YQqw3`2<'
        '`b#xejQJ@`VE<~)c0!hVMtX)N8JynM{LeX0!-2OMvY6?rnDBSFHd3XP7%9d-a`dMa9i=1xs6MHRX`flEWsqBLsy~4A=h!vms*17O'
        'lE=}3JyU+fEb}cIDULOZVr*!hl?nGY2Wcp@O66l7J%9yc!Qx7ci^<j!aSF7HbME-e^X$m9Or(`NV8_hE)X09yqYqNc`&=LO(zG8)'
        '>&HCpTT#&-SQ#>7{X|7z<txRdd#xZm=B>lt9o$0K{Jpwg6&HN4F^!mx4h!1P1Gw6BB15eV4^<jf#R)%BVYT)DV<RIE1Se^p1Y8rf'
        'O%8DxVg<8AupLe^W(<#rk!i?@Q3)qZg9^>`fF$slS|U^6uQ{zZg+kpr2vu74VS7$`+`C?Lp@T`l44)^`kce+f@CnJdUSL@k%aB=!'
        'xkpe;m}`x4hDT6SZuk@giUge0`C}{`-_|NQkZy+ItA&vS4CDGbF`U;-p#r%kgNw?v5371d!rf|9WUYM)ZUM&ausG*vrBx*5JLo3('
        'Z#!1IjeW!Y?%D#lgzU-)?BpQ>8{e6lB4mLq|FOGv)U&|O0+m~`yxi-O0cYA=C%Zz10=J+pQakX-EwZ*+%RF=z?9L%~G}%>o9DyRx'
        'KuDgZJmkhOE#pCB0we;F)(ou$x4|*679-LHtyZYqAXlv(wxb+G5C+;nFyE8luhc>wlTb?|jn`aeJ%(J6;llc@4KkN1OK!h6PaqRg'
        '@TCTQA=8i)d4~SFL4pAkDQe8vAXco7F$4;lfma*;pbZsC(EL6y8^PijBaG?RkNHB)-l*8-2aZZOEHpW4hjD<Un6;P|=mU+rDFlXq'
        '6OC6vA)F~D)>VpSVuy7nX2ffbx=MTE4e=Ho!Fm$2P3eq3+@KqGKi;Usd~xk}T&t&5*ZBr<LvK7v)o$ul#Yw+5s48A<n*!g<AmOl?'
        '9cc*@_v`#*acht07L#!05LXTC-*z<Y7o&?6T4sVg;Kj_LKIjL7rp4kd=EN1TA{KIJC=myxP)<Cm_KP$Aw%p^9kAd=KRBaUJeWP+6'
        'a@dHupD}0`#a}xDDz{@~44Kn;oCj>LV_2s8oo%U;U8Z@*Dixa!sI?FwziFDCEDxY^ea-uMj0z80tm!xwbX4b=ebrm?7QKcGx}-0d'
        '0c)`CeOH;)K6wAX8%?F7WP*}0O`!0VhBkoS#e{`wW>BeiSLsI!bt#xb8tY)yDj`LzI8s_5K*f1e{B`Xg=z$L*`vQs!+^G`iY>`up'
        'i5e)71Z}Bpzjg8L0FTlOCgY*pmWL7?Cc`7{VG|Bw2=KKwK@NI0T-rYUT@|N(E$xT(_a+}^Z*kmLSyhnd2{D5tP!JdJ>K&da*A4GN'
        '88WN%!R$HdhXU%p68DO;_gI8Y@dr%eA?|MEG0f?~)4QVk&uWhLN)x~Y&l(98oyY^YXChOaXF#w$B*t;3L6)FUI*R8;N_x!Ual~UK'
        'J>kB`5JyXT(yfoX^$CZQZhZ>zWJ#wT|0%?YlAcC9QPMMx|19EkNzb|c^N3?5eZk3@L42X47ZA^t^djP!l3qeQRniv`r%HO+oqx&c'
        'z2fw|?Bu-S^u3Dsa!Fr9yi(HF5nn1PLA+ejtB5a_^bN#IC4Cd|VoBdZyin4&5obzz&Dk}Jc)p}_&c1oXvnBnBv-78jr%QU>*}LHG'
        '>p8nSh?6B<boMVHj+b=V-DAc1W7XZKj_dJ~uDN^NaQ^MN``v8fPTz6(GlxHS_^!iWIQ*r<Upai=;g&<;aL?frho3q8+~F4vzjpYI'
        '!*3ma*WjIrQAb>EiMf{OwZ!`^vDFfyCH7k4NlSdz5}&uk7cKF1OMKH3-?qeej>zFz2crN62=;Wh7GOt*Q8Q@|9-8yT2u`fw^AcWw'
        'leb}p+9Quf7+C~H*0Pv=0)i9Phu2Gv@5OhE*_GAB<=*nj>e|{$ue;pqb#L~TmToMrF7;Mcd#l~0wVTV`)zxOC)au6s*Y+`}7GJ@D'
        '5w}qOm*TwmpZHHM*7wDG8{#)V=6o=+)BG&x41X4Mnx6%S=Y#m|K3XU~5Fa+3=dQRvY)~H$sr!eT)<qclI0e&ZcE4h>X?`$o@b|<s'
        'rELnIj)If^1TO>ze*x(I_XaHd{!sTL(EYeUrY&IFI$-j#5&mEqgYJC~moQG7VGRHP'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

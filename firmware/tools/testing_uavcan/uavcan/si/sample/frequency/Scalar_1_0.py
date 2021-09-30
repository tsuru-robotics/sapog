# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/uavcan/si/sample/frequency/Scalar.1.0.uavcan
#
# Generated at:  2021-09-29 15:15:51.618743 UTC
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
        'ABzY8CxcXB0{^X7TW=h<6_#wvy7?N}j^o_uG_|DGJ1ebr<#pP$b(Oja7|VubH$sbc%9){-gy&Y0BWVp3XdYTvzyKW}Qy@PfKOv7r'
        '+lK%J`kbE-^cUo@=ge?+SC0Kw0n&GdJUr*{T&X{u`rFFcsp=<xI~@i(2pv~*C0Qt+GB4zg>nBl~XlZzvpWQJk^G&AsqhZR+&&t(L'
        '%RiPY`HUO02==dMY~N?Gqot!+l)~vf#s84;*dIDOJ`0&D^Er2)D=m|_6jS-^uPpspNvG-5U&>F*e9>jbDCuQ}>+-iC{UvsdxXOIy'
        'uH<1bwr9Z&m|?C#BgKh&QOu0YGcw}N&M@|cN@Dqx2ajMu8?d+(vtqunM4SQb;(|TC^fEhAB_nC%KG?DJIM#9y^WdY{@BvrHy|n0h'
        '(zqdy2S${%4_5k28#hV<u=0)k%7aD_9&@%}?;dWUYyMn5Eb~h)*cb;)1(Sk~G7qk{7)f6xn)^u{l=&$)Nc?j5zbB@q9tlq3Eb_P_'
        '$sU>D(!>a6h+zAiq)clb5G`Y$6P-kyFa;_UQ$rHLXKaX!fxqH3&H@Ux>mW2yasb;a(&5g{iVGb~Jf`_7k(va2Pl8WK%2kV{X()YW'
        'Am$E1F@B~L${8I&O_}Bk5GdktQss{}aC}cC(O9}3g|8AuA~1}rn?!S7G5HC|)hS$5#sgSY`x5R}nIbFg3vdfCZl8r2M=MQ2V!n@V'
        'f<Jp<a!}hh+V5?)z$N5B24E-m8QA#V!U7>J()nF)^SEb$oq0)SNT<{9ks)VF-y{b@`U1D0E@Cru$Q`oTtz=G|1-moI9Yqe3EDS&q'
        'XdonuWA1aUnUdkKHUScWNTWyAg4^I2Sc?(qfmS1uOe0sN9=3xFL=XnrKrla);IG&~9ur?lEwxi$W-EkTkbZ0H&Nf+z6GQHPuu32k'
        'V(_H`eLho=6j_S?x<$Mp6e(&<*)U946=Mh#Gy|tH{81As5~2A6VAg_#Ax0R}Z4mNS#a^q}<6}of92V*vHKRB{QY;%x3-p1)-53Hx'
        'z=_%^p%BjHb6ZJ_WnxBkCzixpmby;+;vMlWox*w&%XR6@KHjF=_dnS##cF=z*IXsftFH15;)dRM5+?_-Q|71L%AhiTvuO(aFolG}'
        'W_GM4%ss5~lZA~vqL<IZm3>^*uz%Omu%Az_m1vpvGLPp=6MfM2hINa@Tdas{VnehtXea>(rBF^hD39`U?w&m4fs281Wl(PC7hRoX'
        '%IB~VayMnrE^^T}QQ97|Cz)xX<*lbt-0keIh3z!+pf+8_2U&<B$4ykX>hfyW4YZ9OX}_?6I_u7wQ*%K(bOqC(77N_9C0HJToBzFC'
        'mozFMr~vZ;Dm+n8@90L%Oek9hC20;4^`uqhyq?flMWs>+xnRVx8Ug`HnAKHY75P{Xd<Z!ZP(|RkB!U(eSjCu;UILP!|1^EJs<M6H'
        'NmNUx+?RWDB9mbRJmC&@TQ7u2-e@vm+??Uk=K1e3Kl5{GKCZrZ_$W>DlWvlhIeD27J&e2r!UJBt$D_oyz57sa%p__&WKO%jfC4YY'
        'gZ%sh7GU@L4wHC{yW3d^19|xTuIT->T%r9!doZfgT0%+ZG7s(<$ruM05bO|%SsY%FEGU#t<GHDVp0Icl@kBvS+3y*|>4KiN>$7%!'
        '&f>gXUqC!v&_&CC263*SXAw^o^ql2CkGNRS3wHk^;!Htbv2vCWUn%G%#0v$zjCih~R}jw>^i{-#f?l=fU$c6zSv{{?Id52fZz8^4'
        '(6<n;74&Vy*9uAyuNL$=;;RLH2k}ZlzlV6apzk7HD(LqSmkN5r+O>>$v7jr~zE#BY1^t1w^M{CM3wqPq+p_m{tle$I`GT%l`_~a?'
        '3)->w*s%WS+WS;-Jz3CAd#_v8zkPeZ+jZROdlr9W@y8b5xA+r_KehNXiyvCtwJ0neT6|{lbBkYC{L<oA7QeRmjm2+kyf-&(iK`8<'
        '(h&WI_^=^%8$vY1VM9D?h|e41i-!2JA--yeuN&f<hWOSJ8NA=1=fkAH=55zJY~3(Z=FRv;xtdSmXd1mE;i)%&7lx%d_Bw>wL|`^`'
        '#PTx`9I*jBQ!;!QzMn5|bk{ol&PI20bEDtu^!vTr{q^-*Yu)w!Mz`PXt#97$^t#=8c2w$T1Xt!Ms22Z(Nh0o`{C|jx;y>bFnb<lK'
        'A8d<X{9guvmhJkX-yS{m+x0_#auA4L9-%4XBk^(FV(yEFqfYe6h<Z5Doi4)|$GH~2u+8Q3b(e#|g8w1BP}+`g=`?ub_b~Gr{Cc4G'
        '@7u8On~63@pv`fOOuN9eJ7#jR<9%ltqwD++wPl}0GYtR$'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/uavcan/primitive/array/Integer64.1.0.uavcan
#
# Generated at:  2021-09-29 15:15:51.373396 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.primitive.array.Integer64
# Version:       1.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class Integer64_1_0(_dsdl_.CompositeObject):
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
                 value: _ty_.Optional[_ty_.Union[_np_.ndarray, _ty_.List[int]]] = None) -> None:
        """
        uavcan.primitive.array.Integer64.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param value: saturated int64[<=32] value
        """
        self._value: _np_.ndarray

        if value is None:
            self.value = _np_.array([], _np_.int64)
        else:
            if isinstance(value, _np_.ndarray) and value.dtype == _np_.int64 and value.ndim == 1 and value.size <= 32:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._value = value
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                value = _np_.array(value, _np_.int64).flatten()
                if not value.size <= 32:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'value: invalid array length: not {value.size} <= 32')
                self._value = value
            assert isinstance(self._value, _np_.ndarray)
            assert self._value.dtype == _np_.int64
            assert self._value.ndim == 1
            assert len(self._value) <= 32

    @property
    def value(self) -> _np_.ndarray:
        """
        saturated int64[<=32] value
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._value

    @value.setter
    def value(self, x: _ty_.Union[_np_.ndarray, _ty_.List[int]]) -> None:
        if isinstance(x, _np_.ndarray) and x.dtype == _np_.int64 and x.ndim == 1 and x.size <= 32:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._value = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.int64).flatten()
            if not x.size <= 32:  # Length cannot be checked before casting and flattening
                raise ValueError(f'value: invalid array length: not {x.size} <= 32')
            self._value = x
        assert isinstance(self._value, _np_.ndarray)
        assert self._value.dtype == _np_.int64
        assert self._value.ndim == 1
        assert len(self._value) <= 32

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Integer64_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        # Variable-length array: length field byte-aligned: True; all elements byte-aligned: True.
        assert len(self.value) <= 32, 'self.value: saturated int64[<=32]'
        _ser_.add_aligned_u8(len(self.value))
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.value)
        _ser_.pad_to_alignment(8)
        assert 8 <= (_ser_.current_bit_length - _base_offset_) <= 2056, \
            'Bad serialization of uavcan.primitive.array.Integer64.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Integer64_1_0._DeserializerTypeVar_) -> Integer64_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "value"
        # Length field byte-aligned: True; all elements byte-aligned: True.
        _len0_ = _des_.fetch_aligned_u8()
        assert _len0_ >= 0
        if _len0_ > 32:
            raise _des_.FormatError(f'Variable array length prefix {_len0_} > 32')
        _f0_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.int64, _len0_)
        assert len(_f0_) <= 32, 'saturated int64[<=32]'
        self = Integer64_1_0(
            value=_f0_)
        _des_.pad_to_alignment(8)
        assert 8 <= (_des_.consumed_bit_length - _base_offset_) <= 2056, \
            'Bad deserialization of uavcan.primitive.array.Integer64.1.0'
        assert isinstance(self, Integer64_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'value=%s' % _np_.array2string(self.value, separator=',', edgeitems=10, threshold=1024, max_line_width=10240000),
        ])
        return f'uavcan.primitive.array.Integer64.1.0({_o_0_})'

    _EXTENT_BYTES_ = 257

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8CxcXB0{`t<S#R4$5Y{awc49k@bEi>rDrqd)u9G<FrJisx-Ly^Gz7+%|ZB3#QCGarf0s)+d77jq51iJY@e)L~x`)4}K<!VXE'
        'isPdX1!@QuwL8~0GrRnj+$_BM>_R5`3$FAx+HSj3(_QLVM#uWaXm)5#Z}qzUo@;rO1t*?*j^FZphkm!wr|b`Q`vrT>szFh=jV{ht'
        'd}F<3*tNc6buG_Yr!~WIjE&ltwnx{fbAOoyn!ZjQ*Xr5K%mn2h;_E*cWFhk#d%=PU-S9leYWf~^*^g{oR0AOv6u+=&r>&wnuD1=('
        '&^;bvaB++}kBbFoe=u+qN4}!=nrD8@N7K+w=(Iz-)b?U~W5O9AX2Hx;Yt5$Z7<1a%gx<6~y%RZO(7;ezhU@9wUYj!WLU86AX@;xS'
        'KE*l0r!YO4U)d8DoYq~>u-k^yP8!<so53-()Hhm|x51zioQkLPpLl9S=xBfTd)plwoOuN_vtnL_EO%wz;8qKIv*WVhrUb2=B7Sf9'
        'Hwz{|u{@E=r}#6r9OU(0ADd&G5qG28>~*Xb3uX!J_AsR$_QcnH>KI<nQOPUmEz`n6oA-jbPkVOD@Tk43C{G5Lbf}FTR7Lrz$9|_{'
        'I2$99C4JrK_>}$5s-T5#(|iyo;}L3|ePY;a^a<@#&l(rf&wAH*hABsdPohEdb8f4FwxaxXEgOr+FHnqRw4ltZ?RN~W4_Pjo2_YAM'
        '=c8|23%L*q@mO&%26-riP!hj${JNZ)gCdkd&|<w~BXdwjjBtFQk0bbdVplmh2FF8~6muH)bz-a>Ou%FaCsTHD6vw7ss{<$CWC+u7'
        'yfb^s!W2x0aB9R4&fxg$8|lLgoC@KzkS*Z+B-fpLV_leq(;=MMH3po;xwHGS1#@sFgmXe?n%Cp}zV+cOoD1Q?*qBfP=Pw?}E}Vx8'
        'AzVu33un>Z<pbM;i*PA~w_Y1BN}<e^L-~Nq@Ky+wxWC>$v@N&-l@P89JC)Z(&i!5+_NTnPp)YtFu7+@3`b%V==jMj8pF}f?Wz>3X'
        '8?M3i5N_^S2aKkI(kOc??K7RfsYq)S&*exz_6IlMW(ZY@Nkbj%rQ4%eq+N+*Hi}1Bl{u1D(I(u2Y6y4U7z=8k{5wK^uTB`MiNwKu'
        '!fm({!d;2yI(n|A>ohO1$*$898IwK~GU?~)z{hQP2kwSY+ZQ&t!*%LXCm(5*2fkHK=TbQp_=M*O8_Yv3gax@jVgD~Go2pJCXB^F3'
        '6wUc49$6!9Pvi=bpv5{Ygs`-4JW%6$@9w^ihpRTclHyv$5g?}JWX&|3oy3_1RkwS|o*b^4T2(Sm*@<zzc&xAl%OTu95Kf`{K<>M0'
        'eJ63MHKzJfVO)ZDVHxhh{Sa2vdaI)D0$+0v)3#;j%bu6Jg|sa5SL4-#MQ#@!z)A>@4vY^ip#FO*&mxj!hl;&K#3Cvw*505uBa~4b'
        '@2h?C`k<a1>uL0K4pw+gKTy3ZR^qY29y1d~JQvqg?ONR5t;p8`db$q};r$RkJQQYl#BF?ZME9eHxWD;$n4r)4h8-QKqA`-m!Y0|w'
        'l1z?d3S<*Mc#$WYd6FrT%_7N^$YzOT%4D+)4cI1)EZNSIMvgQJWE=nI$u@opNLxvxNVbclQ6k$V(kPSda_BcH^5t*w(C~z4n)&oU'
        '!)G<#_5U)T)&A$RQJ$y&=d=F`pVf|-&sO%@&356lrCs>nIL0~5XDjLKC;05B^(2<v+2!H*Y<7&#boS(ZVVDUjK3j=S%H#NK8p|l}'
        'yEL#W+2z6c>@cFeI$?J{%kd~~G|Fdl15T+<9n*<?N&5<y^l|4<d^S7ao?7aRAUr48Y%-sMG2Bh?Sq&wtDL$Lz$f`;rUmT4(b0~&<'
        'w0w4S{SH@a`1B#z*iy`AlQp{=Rc#@~XR{IWQQbIPvGn=l=72MEjEkI49s!?Cc4l&ICy}c4rC9r-WVA7#73-}UarRL@t8B}jm)$Oz'
        'va}p$@QC>=k3(cxM3L-Hv4@B_L>&cV7jbZA{V3+MVxN3HpUt9#>{_t~)oEFt!$d`|4Z4>5t4F?8;JqW{v-`gP44<cCKC6Yk`3f(H'
        'Rwi2rj%Zo3m4z*$<%m`wTlmS5odQ`clAR)1Es>oPSuK;DGSTv6D-Wx%Lsqk7CregyWVJwc@PD4{<cU@!TScOk$W{qiE0S3LoYpJ`'
        'Me!UsDCq58iv=0xH;rI6@h(DdZiu%W&zbqBIpYQsdYkqg${$0w*~{Rh{*(2Lw)K9`@pP-r9tShJ+w+|k#fc8p`-W$-V6E<T`}Gau'
        'XWyIWPs8Vb>DtRn>kFNF-*0xTmhR9szr#(cml*DR*Kj@R)WzGC`rutdJ$j2#AG}?uE!GxlLWp7Prs1MjhrhdUsk3giD0^xCW&Ul}'
        '%ti62dO7vDd+Hmb-L~wtk;mLPyAo(<E1G7Y`Dxy7zIrV3So;U1)9!~)8UO$'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

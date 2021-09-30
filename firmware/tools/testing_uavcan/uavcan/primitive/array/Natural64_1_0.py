# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/uavcan/primitive/array/Natural64.1.0.uavcan
#
# Generated at:  2021-09-29 15:15:51.385175 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.primitive.array.Natural64
# Version:       1.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class Natural64_1_0(_dsdl_.CompositeObject):
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
        uavcan.primitive.array.Natural64.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param value: saturated uint64[<=32] value
        """
        self._value: _np_.ndarray

        if value is None:
            self.value = _np_.array([], _np_.uint64)
        else:
            if isinstance(value, _np_.ndarray) and value.dtype == _np_.uint64 and value.ndim == 1 and value.size <= 32:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._value = value
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                value = _np_.array(value, _np_.uint64).flatten()
                if not value.size <= 32:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'value: invalid array length: not {value.size} <= 32')
                self._value = value
            assert isinstance(self._value, _np_.ndarray)
            assert self._value.dtype == _np_.uint64
            assert self._value.ndim == 1
            assert len(self._value) <= 32

    @property
    def value(self) -> _np_.ndarray:
        """
        saturated uint64[<=32] value
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._value

    @value.setter
    def value(self, x: _ty_.Union[_np_.ndarray, _ty_.List[int]]) -> None:
        if isinstance(x, _np_.ndarray) and x.dtype == _np_.uint64 and x.ndim == 1 and x.size <= 32:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._value = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.uint64).flatten()
            if not x.size <= 32:  # Length cannot be checked before casting and flattening
                raise ValueError(f'value: invalid array length: not {x.size} <= 32')
            self._value = x
        assert isinstance(self._value, _np_.ndarray)
        assert self._value.dtype == _np_.uint64
        assert self._value.ndim == 1
        assert len(self._value) <= 32

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Natural64_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        # Variable-length array: length field byte-aligned: True; all elements byte-aligned: True.
        assert len(self.value) <= 32, 'self.value: saturated uint64[<=32]'
        _ser_.add_aligned_u8(len(self.value))
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.value)
        _ser_.pad_to_alignment(8)
        assert 8 <= (_ser_.current_bit_length - _base_offset_) <= 2056, \
            'Bad serialization of uavcan.primitive.array.Natural64.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Natural64_1_0._DeserializerTypeVar_) -> Natural64_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "value"
        # Length field byte-aligned: True; all elements byte-aligned: True.
        _len0_ = _des_.fetch_aligned_u8()
        assert _len0_ >= 0
        if _len0_ > 32:
            raise _des_.FormatError(f'Variable array length prefix {_len0_} > 32')
        _f0_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.uint64, _len0_)
        assert len(_f0_) <= 32, 'saturated uint64[<=32]'
        self = Natural64_1_0(
            value=_f0_)
        _des_.pad_to_alignment(8)
        assert 8 <= (_des_.consumed_bit_length - _base_offset_) <= 2056, \
            'Bad deserialization of uavcan.primitive.array.Natural64.1.0'
        assert isinstance(self, Natural64_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'value=%s' % _np_.array2string(self.value, separator=',', edgeitems=10, threshold=1024, max_line_width=10240000),
        ])
        return f'uavcan.primitive.array.Natural64.1.0({_o_0_})'

    _EXTENT_BYTES_ = 257

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8CxcXB0{`t<TW{M&7S>%%?8J5)=blE*RY`5hb{yADyIZvZ7G9iAnoW26wjd~JY7(U=ffpk#P{4iIg$oc^0-60ke)K<R_uuRp'
        '4o5>uRvcgYP@sljQ8VZEopWaR4Y^zTZ{tQT{tNF6cDi2IZs;C$EyK2cFxob4=$(FV(Dy8#vhcz;z8iG>z@>lR8Bq3?J^qRP$m(HP'
        'cZ?p+*8*d^V>pe0YxOMO+NKS|b&Z|IO9OQbdwq?Cn!Zh4&+0qO%!So&lk2w(@{s#C`-z29y5ak-)ed~>v465jQ4NJySpJJe?XHUE'
        'yxui@L-%=z;mrx^JT4Yq{no%y9QlemTfX@PAI(C$pi`UnsN*O0CWJFY%)<G9IG(lT(C%LypKeh%Yi~+#TfT0`?ijQ%*pA`(davK5'
        '%)Aj^c_j^TwZ;paBYX-Il=~NZ&BDvN=NnGfaJy+kdqF!qhn5CL$MSa=)WS>2l>Qx0jtJhoC4w;TfM(XryO8H5%?Dh&q_=I4g%2e>'
        'WgL<EqrX`={iWrLq<w=w6L?`!?+>sICK>T|dhNb#budYU_WGDSAFKcMfVzg?cU6)qddIY|q~_Cb;YHu+7(R6l73HA0q)Q#_l{(7L'
        'ybNsHaCgQeEBdx!2bBGX)j^BAw)rec#s+F#eQh{f^fet&-<lNC_j=EGgQ-P@Ry=6F;I>+5E6!ifa<EAJ0>wy93#+`Ufo*Vo$aC3T'
        '1cl_g7=L5e7a}MnW98u(6rmJBMf@)C>uP2W%20_wOZ3i-%|R70!ug>-j^OX9L*?KcoR45y%xT=$g^6-71=A5+%-F?I9GiKk4qSkX'
        '5zHp>&K)TWGcX&$r7=G^gX8n>r4Ms(DT2#FwuJN3TzBEUbzvSZM{woP7;qNnt{%%4EWnirt_hu4UXSa?)`zQbErJ^pV?qg>zj-3N'
        'a2;+$a4VB9oJD)LPizlv!mS8CcxSvQg)(<e<pXZR2NBeg{`&CLw%`ubBDgE;)ZP_2_j_;DpYryezTiW+8^L|)FO_|sn+M8%8qGMC'
        'aqEd~xCi$mcz9$TFq#@lqwJ%s&uso?Vy$sJw`2XpA3T7E5!59n4Rx@W9*<*@b|sSeI38hD=15vaoA3zg5j=TsEU1C<9|`%RI$@+H'
        '5(oDQkKsuKixSU$^jy!@X-Q&}U8kioCVePm($C$YkH_#4EJn~c7B+aob(&JA7;9CBzEw^aGC39agy$F=EI}iJWw}3L|F0;Us!k$j'
        '9L+);&Gk4QStD*w<O-3X#U?CAuzGAf(BOJc4`0WlRU2JNNv)Cy5Yt+^W*W{;<IJ+E+p}~}j#f>rDjBEj#H3z4R#=6#2-Z)8Q|Nvy'
        '_g%HV(>T={Q+=s0uEJATgJ-ZF!G>CIb<|zvYwnY*ZQ1#<=jCo8EzA5hc=cd~+l7x|BZB8A#)lSA|5KG`5lOm3#a<#}5tS5cZ`hkL'
        '$~cbC)INECSWk}iGJ3iO8@#4}QoSoy;<@1-GZ#m^kknM|THN2G*w-?8T8B^Ivk3ltD$MYl+xYy9?nf<ge+%%?K;H}uCq6pGV<eY{'
        'U9y`exdO?R$S!{HqDXd&Bv&T8Ws<9q-3rN7$!--|uuocfvY#id0%?`VKK?I~ef*S=wvtwv?3YQaLiQ`9RVDk?C}>mU%U|Q6;T6#|'
        '^KZW!KCAJr|Bd;q_6MJh^E~?ppZ!hvtaiqHwszERb_k!X9K!!5G0sswTgzrY#b?K@r?DK)E>Fj2^Amh#vnTHhqfAio*;;&3p2TOf'
        'SjKtZt)W%PE>F&9M-d&>35WApjz@8$aXwoZa!PgTm`&wN+E=)wk0+<%v-u(S)G}uT;W^D_)A<yPVKK#LHI%Gp_-vXZt15|naWv}8'
        'p&0Vn^4anAJ6f&L(}!SVs|lY?*K9Ga+H!`^=40lgx^c8(+4IN4A!p_oS2&+M13sJX%=Fq$BUS55vGx_oXcImw)>}R1?Bje^*_J&o'
        'yInG6X*tQ@8S_~lhsd&sBHf*04-s*QIts=v;^55sdBSJKKKX7wn@0)RwPFpb)3Q8=iHhDEb}jeUjD2mur)S7#kA43cJx?cmR*M4j'
        'EnX0<O7;*O(eh+34|_x_5UoV^@KYcMC9+v22W7HZAqN$*StSQmq7}(r5jNp~Z05;9o@^G#W{Di&{~|dk60J=3%0#P>y$Z5cB(eNC'
        'tyvDs;yG|w(!2c*3v(=J8{vHFt%Kg)5$`j8WacmCoEJ{%T{>_ne+=DaKZh6f@2oeps}K6FuUlRAGMv-Be&BW}PS{i*7{1BEt)|}_'
        'G<S^e1AmD>4PW}9=d7)6FWb#Q(6+6P?$WKm<|fta3U8@rcs_NT;yp@p_*S7AzprQx-=j2E8p{nK#4vW#@X)Kv-%@zg-L^WE{cQef'
        '{?A-Ao8nRRYUXkG%qyeYwVbW7$J{u(9%^VSo@Ss0S>A8HeJS$T_&*F7LAW^@000'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

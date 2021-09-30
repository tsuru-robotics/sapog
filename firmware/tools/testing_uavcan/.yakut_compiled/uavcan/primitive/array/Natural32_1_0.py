# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /home/silver/zubax/sapog/firmware/tools/testing_uavcan/public_regulated_data_types/uavcan/primitive/array/Natural32.1.0.uavcan
#
# Generated at:  2021-09-29 15:16:17.697503 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.primitive.array.Natural32
# Version:       1.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class Natural32_1_0(_dsdl_.CompositeObject):
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
        uavcan.primitive.array.Natural32.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param value: saturated uint32[<=64] value
        """
        self._value: _np_.ndarray

        if value is None:
            self.value = _np_.array([], _np_.uint32)
        else:
            if isinstance(value, _np_.ndarray) and value.dtype == _np_.uint32 and value.ndim == 1 and value.size <= 64:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._value = value
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                value = _np_.array(value, _np_.uint32).flatten()
                if not value.size <= 64:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'value: invalid array length: not {value.size} <= 64')
                self._value = value
            assert isinstance(self._value, _np_.ndarray)
            assert self._value.dtype == _np_.uint32
            assert self._value.ndim == 1
            assert len(self._value) <= 64

    @property
    def value(self) -> _np_.ndarray:
        """
        saturated uint32[<=64] value
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._value

    @value.setter
    def value(self, x: _ty_.Union[_np_.ndarray, _ty_.List[int]]) -> None:
        if isinstance(x, _np_.ndarray) and x.dtype == _np_.uint32 and x.ndim == 1 and x.size <= 64:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._value = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.uint32).flatten()
            if not x.size <= 64:  # Length cannot be checked before casting and flattening
                raise ValueError(f'value: invalid array length: not {x.size} <= 64')
            self._value = x
        assert isinstance(self._value, _np_.ndarray)
        assert self._value.dtype == _np_.uint32
        assert self._value.ndim == 1
        assert len(self._value) <= 64

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Natural32_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        # Variable-length array: length field byte-aligned: True; all elements byte-aligned: True.
        assert len(self.value) <= 64, 'self.value: saturated uint32[<=64]'
        _ser_.add_aligned_u8(len(self.value))
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.value)
        _ser_.pad_to_alignment(8)
        assert 8 <= (_ser_.current_bit_length - _base_offset_) <= 2056, \
            'Bad serialization of uavcan.primitive.array.Natural32.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Natural32_1_0._DeserializerTypeVar_) -> Natural32_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "value"
        # Length field byte-aligned: True; all elements byte-aligned: True.
        _len0_ = _des_.fetch_aligned_u8()
        assert _len0_ >= 0
        if _len0_ > 64:
            raise _des_.FormatError(f'Variable array length prefix {_len0_} > 64')
        _f0_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.uint32, _len0_)
        assert len(_f0_) <= 64, 'saturated uint32[<=64]'
        self = Natural32_1_0(
            value=_f0_)
        _des_.pad_to_alignment(8)
        assert 8 <= (_des_.consumed_bit_length - _base_offset_) <= 2056, \
            'Bad deserialization of uavcan.primitive.array.Natural32.1.0'
        assert isinstance(self, Natural32_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'value=%s' % _np_.array2string(self.value, separator=',', edgeitems=10, threshold=1024, max_line_width=10240000),
        ])
        return f'uavcan.primitive.array.Natural32.1.0({_o_0_})'

    _EXTENT_BYTES_ = 257

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8L4#Cb0{`t<NpIU$5EgePj<Y%YW+rhGWs|bUS*tcc;bJ;TnzXqUG$p;5M5zTN<;DS0IENMvK%fus>)l8F4EN@L(Dvq|e@2I*'
        'WJh(J#B0#jzKDD?-^@4j9w~jEarL*~k7ZhaaesZR9G3l@9kRf4eD9@G^jXd>)hhK`=tWG#y-%Z{QHmM?`*y6(#H2X;TD%h3ShK56'
        'h3r<t87(>0Ts`nAUgV9koD&4jSni=i7{|YQMZ~5(%7W0VRfU_0jc4uaNdXdMei5%l++#aY6nMo(#6t1CSc=uWlZdr1J?57e*le}S'
        'PUP58LNPwP1U%s-;{DGYTBVh*S#>0GKTlS>OY60n&nm1Mwc{;8XTD+)_kC9ly^$&_e^rgx2n)L7_1Hx(vi(*%0Tz)hIbmd1YGo$e'
        'L-D@Hoj?gJ_ke7en5aRSpT!dq@3F(ksg|9f{C1#;Mls$(k?Ky#i^c>L;@xeN{XA(-O5Qz^l5qRMbS?J;NJ&WdRDxFRq92O*bf>(9'
        ';8bb!&wCMX`@)OTrah(Gc6qU4*Xnc(mI@M%Rf;v=D^Zh>Rch3{h<5)`odr%*3l^HB+a=edEp@NPdmq%QB`0Flce*A;C!PVT(pkxp'
        '|Bi<Z-*<wsMV`7n>i7*Neid0Td02F>x0^9YsQpiz>Ii$n>MZh>qV$7Zab8es2~cP)x(||A7R74yui{l{ladQ^!;Bdl$*wkhC&7c1'
        '_+~iB?N6okNvB@sptjev`87~L<)Ekca&m2S*+2uGgW1MyS!4r)YJ{!xcv_+Ro_G4e7TC&RTWT|tT)j*BK@V)>u)QlTt<u_#_hO(I'
        'wsY9o=DX{IzOVy!a@f5n4_Rov@1yXr3wCqZllrP;-<Dwael!;PU=N3V@8m#Mvh811EZ7VCI2`EonYbKWHXioF0S<?j<U}51KfI#2'
        'a1ai0IMUTGvQoUGD~<<;;RuIg@8wHg<kP>Z9B>qlaj@Fw>-ef;K|ej$a3YOky^nd4_vD)7gX3_5!$2qJTRV{S=hT|zfRix5;q(Xh'
        'gb)^alkb@|%?+pEG>2@bPI?lOGj?{(bHEwMaya+VbrOR7&#wy)I1A@ETv*uK0g9P@dw(ykTV6O17dYgW)dxZmCcmzn;3DKWTuO87'
        'OrE#P>z)ttaEZf}W%q)RguA*S{NOTN;c#v7S-C*5FLln#^$p_!SK%6m8!PG=p$U6)L%G6rxWQp?;r)_r^^M*!w>F#y+=M|6w^!Ud'
        'ia_`~pM*Eug4-PKE`1KKQI5gnEZ+NM{NN7U<#2yh{iP@r<Fij%1KflA9187T^9IR6_M+}oTjDrf9mkA>;}T|M9G5Yp;JAVr6~|Q^'
        ')^JwCVI60695#r=6j~BaNodJ9C8MR_l!BIuQz~Z2)xdELGdhmzn4xO}3NVcY38y72$T%%yLBVMS3o1^lXpyUlQyN-2PU&bFIAy>v'
        '%;K<wvl0%=I4k3@g0l(^t2nD-LBnYc3p!5gSTJzf;Ef_9we^T3=VLTY_nUu>8ZwjL!RxGs%uO}a`URNTR72~chRiiqL)M4hv+JOS'
        'tnMB7&#ECS{lCEfN)077543i7Qw??0kV&ZQrW#tLhPuznrW#tV8cN?US+eciR70y!L+SU?rW)D^HAFq;4R?|*F>7FxNT4a<gai|4'
        '$~YmTso;cyriv3P&Zsz~;f#iJ5)SF;$~dFroQy*Tx(d!1#Gr{;37ZmTWo*irRj{dGR>h`@u8MOi48aTzNjO6R2u)DJDLAB}Nl_`4'
        'hNg}aI+_Mf7&u2sC^nfibSafV0tZ}}LzgmW*wiqqV^b#yl+1`+E!NT*RIJ+NT1mti(I`4`-&+$;yEvB4QeO%84|i7>_t<4t4_Gn+'
        'D~mVrcKf;af|c!hEr@KdEFQ+Y?6B4dN{kFXv+GXeiuk9zTdS~q==q~8$iJi{FY=*NuZ`rNdqL$#Ct&%gR`bI=WsJP)h@H-D^Yup2'
        '_eyraMjC#SaAA-d<~uH(`DDH|Le0;Qc5|0=mvX6-ppslCBr-uVI1O1a>Xn#y<NoRX<z8^}>GbSM*930IW2amuDvKs>WW5oa6su(x'
        'U^cqNq&xXAZEx;x{u|NY%pL#$'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

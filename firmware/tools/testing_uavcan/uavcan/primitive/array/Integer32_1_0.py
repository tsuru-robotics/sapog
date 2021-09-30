# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/uavcan/primitive/array/Integer32.1.0.uavcan
#
# Generated at:  2021-09-29 15:15:51.371149 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.primitive.array.Integer32
# Version:       1.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class Integer32_1_0(_dsdl_.CompositeObject):
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
        uavcan.primitive.array.Integer32.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param value: saturated int32[<=64] value
        """
        self._value: _np_.ndarray

        if value is None:
            self.value = _np_.array([], _np_.int32)
        else:
            if isinstance(value, _np_.ndarray) and value.dtype == _np_.int32 and value.ndim == 1 and value.size <= 64:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._value = value
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                value = _np_.array(value, _np_.int32).flatten()
                if not value.size <= 64:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'value: invalid array length: not {value.size} <= 64')
                self._value = value
            assert isinstance(self._value, _np_.ndarray)
            assert self._value.dtype == _np_.int32
            assert self._value.ndim == 1
            assert len(self._value) <= 64

    @property
    def value(self) -> _np_.ndarray:
        """
        saturated int32[<=64] value
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._value

    @value.setter
    def value(self, x: _ty_.Union[_np_.ndarray, _ty_.List[int]]) -> None:
        if isinstance(x, _np_.ndarray) and x.dtype == _np_.int32 and x.ndim == 1 and x.size <= 64:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._value = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.int32).flatten()
            if not x.size <= 64:  # Length cannot be checked before casting and flattening
                raise ValueError(f'value: invalid array length: not {x.size} <= 64')
            self._value = x
        assert isinstance(self._value, _np_.ndarray)
        assert self._value.dtype == _np_.int32
        assert self._value.ndim == 1
        assert len(self._value) <= 64

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Integer32_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        # Variable-length array: length field byte-aligned: True; all elements byte-aligned: True.
        assert len(self.value) <= 64, 'self.value: saturated int32[<=64]'
        _ser_.add_aligned_u8(len(self.value))
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.value)
        _ser_.pad_to_alignment(8)
        assert 8 <= (_ser_.current_bit_length - _base_offset_) <= 2056, \
            'Bad serialization of uavcan.primitive.array.Integer32.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Integer32_1_0._DeserializerTypeVar_) -> Integer32_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "value"
        # Length field byte-aligned: True; all elements byte-aligned: True.
        _len0_ = _des_.fetch_aligned_u8()
        assert _len0_ >= 0
        if _len0_ > 64:
            raise _des_.FormatError(f'Variable array length prefix {_len0_} > 64')
        _f0_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.int32, _len0_)
        assert len(_f0_) <= 64, 'saturated int32[<=64]'
        self = Integer32_1_0(
            value=_f0_)
        _des_.pad_to_alignment(8)
        assert 8 <= (_des_.consumed_bit_length - _base_offset_) <= 2056, \
            'Bad deserialization of uavcan.primitive.array.Integer32.1.0'
        assert isinstance(self, Integer32_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'value=%s' % _np_.array2string(self.value, separator=',', edgeitems=10, threshold=1024, max_line_width=10240000),
        ])
        return f'uavcan.primitive.array.Integer32.1.0({_o_0_})'

    _EXTENT_BYTES_ = 257

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8CxcXB0{`t<OK%fb6!yFa5(pu@X~~oVHILW<0;Kfif?B0IJ+y_ET{Riom&^!zY|SGgNJwGPDo7*sO1<o}%+K&Lf1&Lr%lwR<'
        '@i+-?Fc9)UZIg{>&f`1ZJ@?MoU(T%hymczq{!50NGu5zKE7&0mJg4S8cFHwYuq%yvvk`g`6Un}NQ4m+6IAA}{G@1BaoPR2wh<u{i'
        'zEdZ^6+6=v$1gMkukJ<OG%Gkk;LH@h@gp|Hf~!|VV%pOz2)%|c++1SZ?_B>bK!V(_;;BgbY$u8WuN+4#6hDhztX6|WqJ8bLT6K-h'
        'Uc2f<jvb{GlaoEtQ(huDdfy={S-xfdROEh{TDzCF&t^4NXMWVd>p^FA#UdHJ=S}&n+F5fqTAy9^BD>ZuCcq-96(@}BdZWsOdm=gV'
        '{R&K)R=7<*OkLET+%Mv;NDkRy<oH!5sJ;j^7nhSggw%8@UNj@1lpO51><4LUGU|js^phX<B<Bu;>00h-kkV4_*%Vc^%e7D>=T;WI'
        'R+QEs{qtTV{kOa*Yvnz<?I0(L-DuL`=miqa)XR;UR}sk&vU-DB8qt~fuE_!?Y6NS|)9s4u(MG%1lEb$fe#MEH|I*O38EIs|d^$mS'
        'iXXTW*J@5Mvo2D%r=42N#BU-GCJ)Q*jZQOeQr6MCjz7ijvL=hXUX&i%b>|VaoDy!ejqX<|mPJ_Y{?$F7HZQ%PFwB{Wk?wX}bJBc}'
        '(%2jax$~*CKj~SJIj9|*wrT?fR1SJ}FQ?Z=mk%`1IhdWiJ?ng6&>CUyYCc)$zVD@Rum|>X=+As+T5Dg=IOv0Z4*R=s$x60?SLVPz'
        '*w5iWhwtEPV_^Uea5%WG4tdBv^hWtG2nRVF%3@XW_oums-#8bB;1Gu+FXcd9@*Uj}7955n9FDE@nYbL^a6TM`V;oNO<U|qVKlxU;'
        'a2!r>c(1Ep<R!fK-x?22!h0M}y^=3QQOxkBYQXz&ii6cTUmt853x?^rhSM32^(y9R-4C~<9((|&Ih<Lk`N9sQ{W-g3HQ+-y!{OX('
        '_k=Pmil*3)wzM{!g>xM8E9;~uAw6T~x4Z^?1bGe@-gupqLGc&2g$JC63mh)3?d=)D%)hw5BimLNF2W@ag$?zAvM8sxt(;&43LHkW'
        '8VAzn?eezQgCdM_xU%71P$uPF-4T9p8Ln^`TYpwA5%%cHdAYV@T;M8<ak&0gJ)>;Oy|JTQ;Tl}$FuwMF$+!DP@0gEwoCn;1aSk`%'
        'x_5*?`JcQK-taNp<nU?lb2vsd#?!O-**oJ0pTMUaKHpS-3577ec&BTC&){<orB1JTOmdMuYC3*fGH2FV%t<&aVNS+b8FLEGDwtDo'
        'R>esTmo%KzaY@HXgGkJyCE>h;mW=Z<S_;l9XsI}_Vva%$oYgR=<E)N3x;CH$Ei6gclCUIWOU9CdEd@&|wp6qz)WmrWEgk1|v<#d#'
        'U=o&aQo<z(CuLlcaZ<r01t(QpQn93AOT&_mEgee+whSJZ8L6!wNOImq({%6sYt)dL{tn(|HDvCpq4qDp+^!nh7BysUu^O^o_nzGb'
        'HDq<~z<*W^S=s*u{#R-!UGtgt?(V9g6*Xj1R(@9vty4qYXJuCnZBz|q@0UFJ4(zI-O{k&l`)F4U?SvYl9`o3JPM4TBaDhmmDdC(1'
        'b7;yqC!?w0oPwr`b1E*XIHBR9hRYI8=;+G0sN=GX69&2pE*ivO0rL_rNSK##LB_m-3kv2{Tu{+faan~4Si}hl7YTr}DV6dRoKVpu'
        'R4S#RspFiErh#(?E>jW0CYOdTl`=@+fD6m$QUwhcG|cO`ppyhjXGE@+XxR)ZQSEA@B9fel%T6-%!W`5t&twzUC&K;19SoB`yULmY'
        'OGjW;@hsVIKky#0s@-e^k?mE*on+7s8*xx!<ft*b=|rwbrixL$S)6em#?eSRi5q!b_s6bGkJgIKxLorpcEG0MS_-)~Kn+LgP8hME'
        'm`!$zt8>m`dxBbAo$MAa7e)(NkRa}^6H?V6otuU%nD#16Jahka|8fiN<!nqg)-`Gy_}-~jJ%4K5h>g7CiAh*(w*WKlR*mlSJ6RtK'
        'e*<NrPhiU)000'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

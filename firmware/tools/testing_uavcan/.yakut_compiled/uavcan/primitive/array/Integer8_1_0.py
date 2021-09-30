# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /home/silver/zubax/sapog/firmware/tools/testing_uavcan/public_regulated_data_types/uavcan/primitive/array/Integer8.1.0.uavcan
#
# Generated at:  2021-09-29 15:16:17.692230 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.primitive.array.Integer8
# Version:       1.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class Integer8_1_0(_dsdl_.CompositeObject):
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
        uavcan.primitive.array.Integer8.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param value: saturated int8[<=256] value
        """
        self._value: _np_.ndarray

        if value is None:
            self.value = _np_.array([], _np_.int8)
        else:
            if isinstance(value, _np_.ndarray) and value.dtype == _np_.int8 and value.ndim == 1 and value.size <= 256:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._value = value
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                value = _np_.array(value, _np_.int8).flatten()
                if not value.size <= 256:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'value: invalid array length: not {value.size} <= 256')
                self._value = value
            assert isinstance(self._value, _np_.ndarray)
            assert self._value.dtype == _np_.int8
            assert self._value.ndim == 1
            assert len(self._value) <= 256

    @property
    def value(self) -> _np_.ndarray:
        """
        saturated int8[<=256] value
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._value

    @value.setter
    def value(self, x: _ty_.Union[_np_.ndarray, _ty_.List[int]]) -> None:
        if isinstance(x, _np_.ndarray) and x.dtype == _np_.int8 and x.ndim == 1 and x.size <= 256:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._value = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.int8).flatten()
            if not x.size <= 256:  # Length cannot be checked before casting and flattening
                raise ValueError(f'value: invalid array length: not {x.size} <= 256')
            self._value = x
        assert isinstance(self._value, _np_.ndarray)
        assert self._value.dtype == _np_.int8
        assert self._value.ndim == 1
        assert len(self._value) <= 256

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Integer8_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        # Variable-length array: length field byte-aligned: True; all elements byte-aligned: True.
        assert len(self.value) <= 256, 'self.value: saturated int8[<=256]'
        _ser_.add_aligned_u16(len(self.value))
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.value)
        _ser_.pad_to_alignment(8)
        assert 16 <= (_ser_.current_bit_length - _base_offset_) <= 2064, \
            'Bad serialization of uavcan.primitive.array.Integer8.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Integer8_1_0._DeserializerTypeVar_) -> Integer8_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "value"
        # Length field byte-aligned: True; all elements byte-aligned: True.
        _len0_ = _des_.fetch_aligned_u16()
        assert _len0_ >= 0
        if _len0_ > 256:
            raise _des_.FormatError(f'Variable array length prefix {_len0_} > 256')
        _f0_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.int8, _len0_)
        assert len(_f0_) <= 256, 'saturated int8[<=256]'
        self = Integer8_1_0(
            value=_f0_)
        _des_.pad_to_alignment(8)
        assert 16 <= (_des_.consumed_bit_length - _base_offset_) <= 2064, \
            'Bad deserialization of uavcan.primitive.array.Integer8.1.0'
        assert isinstance(self, Integer8_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'value=%s' % _np_.array2string(self.value, separator=',', edgeitems=10, threshold=1024, max_line_width=10240000),
        ])
        return f'uavcan.primitive.array.Integer8.1.0({_o_0_})'

    _EXTENT_BYTES_ = 258

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8L4#Cb0{`t=No*VE73S=;<%PDqD0UJt-a;o1Nhfy9I7`(8EmXXIu4=b|F2QI>jx~dF84QOi6~KUUXrTZD^anBqbktEt9d*=E'
        'M;+DnqN9#F>ex42EHkpaOGXpv!kPbV-~YWwQXl7^Q6GMHG12}DhrQ`?qg=_F4cm9Eiu=7)tk_wzRIhsVh8x&Xc=TT2H%md&xBoKj'
        '+0jqY)gPh<Q6|*PnpI`{aMPM9S+%U^yHz)Er|hid`_^>!54FIawEaR9Ce10^Z@BeZ<Rn7l+wS#G5lNKzXY@l94wzOD_-?To*p2AB'
        'Xg5%goT5<sy=zy>+h7ixWh=1EAVwIT-z7YT6@_QNwRn|R{%F@G1LwE#YX8oTns&vm+O?pYZx=X^HXMZ~?zxjSyWHJ!f3^X$=mut`'
        'T`Zy`LoHd2z^vBGcI2E3&y4lb#9`TQ*oN4|^d$Zf-HpOiW+Sj_Wy>!=o@lmN3=eT8&nmgWbcBQyp6uGp`!P2i>|9{*ueHXm=$v6n'
        'IcettNpUUba-3E*i<L$cUg_<6yDAe9{QN!&k9_S09WL+jZ8vkMm~}4-)4L^UOjnEbid%}pLD<zga~kka{K>O@E2#V1?CEC7ak<mZ'
        '&G7U$^;*da?AjAuV>V(>->&fpW!V4too1zC`O`Z*b#uz9H0|hLQHD~YQFLx~$+*o?XYX3IN&Bwt*@3$oq`#R}s}*z35ns1go!`aD'
        'lANqfVAZX0`{IkXUote}em5&toPea*Hz7#wzAEikemBU1)b5)0XpIz71?io8IleafY^0GcDA|oWw8KUQ<D$cl;(3Md2cGChhv=}N'
        'BOO~Zu61-*KN_GTf{yj&<yBrg{?r&cO2-7Hx-|ryc&0ZU=Qh#F9hKO^>x0h~PbcW4pi>=RmF-93*wfD)OM`Su(3vM<U@P0szECbY'
        'O=koR^_XTXZ@q9louwf`=XS-!9&A7VQhDhuIw$DuKEBw>`QCZyd~}}P7WD2@@v;~D48KwhdWYT>lzzl*jQYJ-&Pc<Q7IdMLC;c@1'
        'arKL@r5?RU7X)4E)qJcEF-w<UTMfEMmjqpTW@k7e&ED+${%fsGm+6Y2OmCmvo?U(IHRyfH2>Rf;_sJ3L|KXnCpsVzOpljQ`y~H^)'
        'kN5YZJ*!I}(ltTZ7vh1VI3~BJnCK(Q3d(QKL8dba*Y~_C<tQ)c;}>RxBRTGqeZfc9>0?1Rc23MS&YkZ~&CPwoLZ8qLL7%=9XB^G3'
        'xAqk)-K0+i75b+uAJ5lk`;LQdQ9;n{m*$Q$aQx?Q1UG#~w*`H%`yAfj8ijZkzkFl(=yUo)&{wa-FK6K#zj>p3pfBkwK_fe6mb>3%'
        'DQUMntJap&Z4V@5Bvd4H)*O^XQbtn6mWHHGDWqhiRHSqo!jOz16+=3<3`!#{BdsE>QwA9s85J3w^2p1`tH|qAKtV=9MM0+#jK~;K'
        'F{0BbMrDku7}aSEV=~56jOjFvaT(((#&w#&gp3Il6FNC?WH>4uojiClJQbc!Ewp5`RJ3%O!HkR<6*D@`VphhiidmfmgbblV=ro5p'
        '8FMP;behM!jCmFFIxS#9#)66koffeuV^PJTPD@ylv7};2r)4b5SXQyD(+XB(tf*MgX%(w7R#mL(w1zbqYbw@sTF1JKbrtJ6ZD2#j'
        'hKdcHHnAyVQ^lrETiBAZ#e6cm5)uj$8WIMQ5|Rp%OtOKLgp`7mhLnLJ2}25oGz=L?OGqn7Ye*Z&NXRJ2Xvi4IOUNt8YsecYNGK>M'
        'XebyMkuaiQM8k-IQ3<08Mm3BY7?UujU`)f9fpH1r3dS{z8<>zVp<qJ8gaJo_qrlPN81N)`3Oo&-ftG}pf|iDsff)%i3T8CS7?_nX'
        't6)~ctN|fGC=eQifjJ3t3g$G-8JL$auV7xoynzJ?3knuAEErgnu&7{B!=iyD2}=r=G%Oidmawc~S;Mk{6$vW}Ry3>_Se3A<U{%Aa'
        'fi($h3bquiX;?F`E@554x`uTF8xl4YY-rdpuqk0v!KQ{y16z`47Ht;nf2Ndk7pbIk@Bc<mCu1FTpr`jiPp3LO9O&si(9`_ic!%BB'
        's;AS>`i|ZMJ)Q3F!!K4(r?-Ct`PJy@c+ZzObEdz)ziK@lbCT&z!hxRtnV#;Sm;*iiqI$aXDU)Ga>OfDwf}ZYtD;?<R{m|3fpNL&O'
        '?L6e=$0aoDW+an64J~&yw9djKR?@MEZi{L4P0DDN&#a?kF|9sXM#u8GtE3NP^e<ILcQiDM>F1Ww@snyt3$@Op@K80&^->fjqGr(w'
        '2Om3+VHT%52R$A{&cB@#jc~v$+n#U7PvXnbkKr-%zT2|PrdRg^(=A7L!V_kr-t<d08!EQxS%DLU4{}buYUdhmWy<z*-*b^xu3>rg'
        '$=rR{um0Wg?Oaf=R~k947`U}bvva5<=QWEJw`BVEWU~?%+&<>f$n{)$=O=RQ10K2Fxs&YmY(CrZiFikj)nF`se5#{i`%`Yoj(&9h'
        '<NVjjI@ddo@Ne{;12{frmCKA|$Mb)-7Q!UwYMUcUHv4~%a30?2u$%oKMH?7GXd?gs'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

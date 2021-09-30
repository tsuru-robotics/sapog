# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /home/silver/zubax/sapog/firmware/tools/testing_uavcan/public_regulated_data_types/uavcan/file/Error.1.0.uavcan
#
# Generated at:  2021-09-29 15:16:17.884280 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.file.Error
# Version:       1.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class Error_1_0(_dsdl_.CompositeObject):
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
    OK:             int = 0
    UNKNOWN_ERROR:  int = 65535
    NOT_FOUND:      int = 2
    IO_ERROR:       int = 5
    ACCESS_DENIED:  int = 13
    IS_DIRECTORY:   int = 21
    INVALID_VALUE:  int = 22
    FILE_TOO_LARGE: int = 27
    OUT_OF_SPACE:   int = 28
    NOT_SUPPORTED:  int = 38

    def __init__(self,
                 value: _ty_.Optional[_ty_.Union[int, _np_.uint16]] = None) -> None:
        """
        uavcan.file.Error.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param value: saturated uint16 value
        """
        self._value: int

        self.value = value if value is not None else 0

    @property
    def value(self) -> int:
        """
        saturated uint16 value
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._value

    @value.setter
    def value(self, x: _ty_.Union[int, _np_.uint16]) -> None:
        """Raises ValueError if the value is outside of the permitted range, regardless of the cast mode."""
        x = int(x)
        if 0 <= x <= 65535:
            self._value = x
        else:
            raise ValueError(f'value: value {x} is not in [0, 65535]')

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Error_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        _ser_.add_aligned_u16(max(min(self.value, 65535), 0))
        _ser_.pad_to_alignment(8)
        assert 16 <= (_ser_.current_bit_length - _base_offset_) <= 16, \
            'Bad serialization of uavcan.file.Error.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Error_1_0._DeserializerTypeVar_) -> Error_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "value"
        _f0_ = _des_.fetch_aligned_u16()
        self = Error_1_0(
            value=_f0_)
        _des_.pad_to_alignment(8)
        assert 16 <= (_des_.consumed_bit_length - _base_offset_) <= 16, \
            'Bad deserialization of uavcan.file.Error.1.0'
        assert isinstance(self, Error_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'value=%s' % self.value,
        ])
        return f'uavcan.file.Error.1.0({_o_0_})'

    _EXTENT_BYTES_ = 2

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8L4#Cb0{@j&-*4PR5Kc<dq-hfprK$uH)F7zZ2<#?NTEq*4%LN^m+R^<e@Bpi|y?3*c?X`B-*Sks}iUew<l|bt9!W%FAoy^`{'
        'el$&l&JWglX7`(K#<So2a`msj7w5*0xl@i(m1aIsOmdp>XEe^3PZE)rLUGNkS!ruoCAyNVGb)*VW$!<?KiPX`ffO`H|9V9S2`&5{'
        '$Afh#g|udg447106c*;p;*;t6m2J*9=YF@(t+_#{){@7SX3GA6XqWIf*=5bb0cTly8h@FjR8yiIsmqR+lIL9W0q)r77K--^mNp8_'
        '`b@r_%ncHAO)^&WHQ44Ff+tjIl8cmCxMgl19Rs;zehqz(oeMLX`^~njxkZ$wMM`CQ7U)G4!-82D(5ylRS4k=oYvwFkSItsQ6z+^Z'
        'Apsk3d%Ak3xd!jT`*3H1a3yM5_y9gM*T@v>z2kh@u#`->^1hbsQj2P|(d-x<HqG^(q=~aC^dC&u=r{8ZtV=@080@3}<Fe8Xn_={A'
        'Nb0Rt)Ed)*P55*g1h&n>!`<DT-5C(Chf#+dMBQ-z0<`(<8IYD5(WSKJXQ8yRSF6?AZL(hv8}*B5UD?{10q$l4p&G4vtrNArM>O+A'
        '!)N{{9(Fg&OU+VGGMWZYC0;mB6dv_Ts=?DhwO0yWXys{v)|5+@Xdy@T9GmT}S(0mnPxcNQ`vl+Jx})=`?)Q<7yTP8j)E-w}A+(3h'
        '##65+BvN6Xrn1lUWS1H#r2YntS$@{)LF2GaI#EOp_gY`qFDml(qgjd^bvq<FAnl{Q+Qn#}%~B-Sl<n@(QPk>O+yOhMaLjC+(K8Z{'
        'Cer9&Jy?hP@G*Q24`Cm^gb==g@1O%Q{0KR47=ngh;b$=LqCyo)8D8gvVoTVUW|j2#kfo#)QWKuq(5w?BDw#0iegbh#VvPtu<SbA;'
        'L(L7IRWTg~ik6}u^tjBQQpo}>M5Y3yrg_mP6TJ?~D$aO9B<ok13wSE0Dwu9@QG&6g`&<44e_}-`B|sHMm#olEa0fhL_9gaF5Ml`I'
        'W(VRgx0tFj?TH?C?wO|XM9Jh>oqVT>afWhq_gKzO#S?+``EP4(e#Q0S_`A(cl+(OLL}`t88HgI?vA|rB`D2y~91bpeG^T;m>SPF9'
        'BMEREG4PLh`-r9~7VC{o@UQcRRhCgXI`4(eKkU8c+Mg=M30O`LY;&oKG0&VAZm{5j4&7qW4HvAu<G<`=oEGCD8CJ1tDgQs{$!bWY'
        '2LJ#'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

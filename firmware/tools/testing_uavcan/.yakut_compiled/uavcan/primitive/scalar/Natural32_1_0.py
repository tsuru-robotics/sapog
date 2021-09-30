# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /home/silver/zubax/sapog/firmware/tools/testing_uavcan/public_regulated_data_types/uavcan/primitive/scalar/Natural32.1.0.uavcan
#
# Generated at:  2021-09-29 15:16:17.671708 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.primitive.scalar.Natural32
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
                 value: _ty_.Optional[_ty_.Union[int, _np_.uint32]] = None) -> None:
        """
        uavcan.primitive.scalar.Natural32.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param value: saturated uint32 value
        """
        self._value: int

        self.value = value if value is not None else 0

    @property
    def value(self) -> int:
        """
        saturated uint32 value
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._value

    @value.setter
    def value(self, x: _ty_.Union[int, _np_.uint32]) -> None:
        """Raises ValueError if the value is outside of the permitted range, regardless of the cast mode."""
        x = int(x)
        if 0 <= x <= 4294967295:
            self._value = x
        else:
            raise ValueError(f'value: value {x} is not in [0, 4294967295]')

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Natural32_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        _ser_.add_aligned_u32(max(min(self.value, 4294967295), 0))
        _ser_.pad_to_alignment(8)
        assert 32 <= (_ser_.current_bit_length - _base_offset_) <= 32, \
            'Bad serialization of uavcan.primitive.scalar.Natural32.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Natural32_1_0._DeserializerTypeVar_) -> Natural32_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "value"
        _f0_ = _des_.fetch_aligned_u32()
        self = Natural32_1_0(
            value=_f0_)
        _des_.pad_to_alignment(8)
        assert 32 <= (_des_.consumed_bit_length - _base_offset_) <= 32, \
            'Bad deserialization of uavcan.primitive.scalar.Natural32.1.0'
        assert isinstance(self, Natural32_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'value=%s' % self.value,
        ])
        return f'uavcan.primitive.scalar.Natural32.1.0({_o_0_})'

    _EXTENT_BYTES_ = 4

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8L4#Cb0{?YWTWb?R6ppm9rS(E-@zvA^sV}=$p+7)Dkl0wP`X<B7&S_>~c4wGNObSK&pja4C=n?$6o=uvjR=Q7TIJfU|_UrQR'
        'KTDnImmj)`4AK-VfY;pUV=fF7tg^MUK}W!R_b~cY#pL1r!~ve;lT$pwo!n&&uPMKs_^9Gd;k>SO)FUWD#SQnxfKwAU&!1slWh3xG'
        '+Xhu9uYA0S&#`~2-}#QGnAaJP(QA<+1pI_I!MZHM+<m3N$OW7=CVAv6wis_}zl4Z+^FtH#umSnHi7*8JFSm6jbYupaVN}@f(eR3g'
        '$Z9JA)mDCRFdx*m6)!2b-=>IA=NrDmyv0J~jpSZl9rPm!)y>@zH;E7|GifW#9ZZ7f%`5zwn9QU-LDf?mfzU{B9x5I|;#t1Oj`SEL'
        'bJj<uB@Xfi3pV)*C}Ds(PP_7#QrQ~Hpbbf19@CO>8Mw2<@<{voGxtzNYfUI=W7N%%&1@`P5=K|d!!Vh4;X>9>&P(R(%bC;VrPIZ3'
        '@wAv#k;F{#KxjNPu{C0(E5I|gtsW6~VFKpIbDI_-QDMCP#(d|6j&G*#Lwa7=l$V%wn0q%336ok_;zCIFp|*4ck*@Bo1J9%N3$t&t'
        'N@+SJwVUrBa4AWQ|BBRJn;j%WbSKxdG-2lHPu%JEeg#4I?q-9qznTQmt##Ah5e0nQ1}p6?k-%;D8iTRp&GeTTBoRas#a}ebM;N06'
        '000'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

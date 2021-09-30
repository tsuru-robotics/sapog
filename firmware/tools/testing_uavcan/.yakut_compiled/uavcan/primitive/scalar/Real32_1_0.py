# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /home/silver/zubax/sapog/firmware/tools/testing_uavcan/public_regulated_data_types/uavcan/primitive/scalar/Real32.1.0.uavcan
#
# Generated at:  2021-09-29 15:16:17.677457 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.primitive.scalar.Real32
# Version:       1.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class Real32_1_0(_dsdl_.CompositeObject):
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
                 value: _ty_.Optional[_ty_.Union[int, float, _np_.float32]] = None) -> None:
        """
        uavcan.primitive.scalar.Real32.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param value: saturated float32 value
        """
        self._value: float

        self.value = value if value is not None else 0.0

    @property
    def value(self) -> float:
        """
        saturated float32 value
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._value

    @value.setter
    def value(self, x: _ty_.Union[int, float, _np_.float32]) -> None:
        """Raises ValueError if the value is finite and outside of the permitted range, regardless of the cast mode."""
        x = float(x)
        in_range = -340282346638528859811704183484516925440.0 <= x <= 340282346638528859811704183484516925440.0
        if in_range or not _np_.isfinite(x):
            self._value = x
        else:
            raise ValueError(f'value: value {x} is not in [-340282346638528859811704183484516925440, 340282346638528859811704183484516925440]')

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Real32_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        if _np_.isfinite(self.value):
            if self.value > 340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(340282346638528859811704183484516925440.0)
            elif self.value < -340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(-340282346638528859811704183484516925440.0)
            else:
                _ser_.add_aligned_f32(self.value)
        else:
            _ser_.add_aligned_f32(self.value)
        _ser_.pad_to_alignment(8)
        assert 32 <= (_ser_.current_bit_length - _base_offset_) <= 32, \
            'Bad serialization of uavcan.primitive.scalar.Real32.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Real32_1_0._DeserializerTypeVar_) -> Real32_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "value"
        _f0_ = _des_.fetch_aligned_f32()
        self = Real32_1_0(
            value=_f0_)
        _des_.pad_to_alignment(8)
        assert 32 <= (_des_.consumed_bit_length - _base_offset_) <= 32, \
            'Bad deserialization of uavcan.primitive.scalar.Real32.1.0'
        assert isinstance(self, Real32_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'value=%s' % self.value,
        ])
        return f'uavcan.primitive.scalar.Real32.1.0({_o_0_})'

    _EXTENT_BYTES_ = 4

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8L4#Cb0{?YWO-~d-5M3iH2!4b>JnEhVqt5Kd><1n^Xymej1dJC$Iz7|9JDv1QPr7^7T_TAbG?H|p3FZH_nq^tUFsJHN)vJ21'
        '-h5m5v$jw<|J;*e!VHrEF<c8O#Sx7q4@jc2LK$H>xcdiImx(Pk|2Qc)oWZjbIEGDEB{|J7|G1>1gyun^MJB8m@xUZhQXTAbDqBr('
        'OJu~g5h{nY;ub$$#AndI)vx@36L2epTB}7|T5jMFZrbUx2wZhraLMMoEE7g8CDt!^Q~Tw9;O=fqMeV<IR!A%?kvt#T6#6xUOsKIW'
        'Q;b8p?jG&U+I?H_7IQm3g)}PPVISN&F_z|xYIYUqC*ovum<wAnKX{;NVv)W<S+*}?#Bdv}sNU=~TT!Re>b0A_UVE$8XmsmQqt}Xh'
        'QM=LEYPO@O4t`b{r&U)SQCTA70%0lv*LgQaG&!khUTAK3ZawRo$SohD;;(9-Up6}3ZnxR!yr?~&g@=em-P#rXNj#a}^%&BPbk(3P'
        '%p)e$at5dF0U3xfXQWWt62V~CtrDY3op4M@P6~>w-PbTx84rz+c>3@Nhm1o*3pES}LT6v7=Al(enh+;ikq^n#Lt#<IQY1w4VJZE<'
        '`B_akE1BIPoZ2j$+AL@U^<Y{8NGPQSSJ5bgcfm*`98S|sSMhqq64ie?Gs*l|SZS}n!QFc!?ECZg0X{G6;%*aFfUDgEVkTLvkO{7`'
        '!!v~z^oRaXa80e!bJN`+Nh;9D>6UxAM;SvY{wqpf`|NHhk?iDp77?aC_ywE&+HVu%-&Rb4pubecNH-I?_cI1`?1M$`X_VJ@FB3j4'
        'Xny`f?v}BM%Q*N8V?@JX9s~dY'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

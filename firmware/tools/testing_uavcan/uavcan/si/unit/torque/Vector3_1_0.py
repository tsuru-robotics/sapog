# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/uavcan/si/unit/torque/Vector3.1.0.uavcan
#
# Generated at:  2021-09-29 15:15:51.528685 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.si.unit.torque.Vector3
# Version:       1.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class Vector3_1_0(_dsdl_.CompositeObject):
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
                 newton_meter: _ty_.Optional[_ty_.Union[_np_.ndarray, _ty_.List[float]]] = None) -> None:
        """
        uavcan.si.unit.torque.Vector3.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param newton_meter: saturated float32[3] newton_meter
        """
        self._newton_meter: _np_.ndarray

        if newton_meter is None:
            self.newton_meter = _np_.zeros(3, _np_.float32)
        else:
            if isinstance(newton_meter, _np_.ndarray) and newton_meter.dtype == _np_.float32 and newton_meter.ndim == 1 and newton_meter.size == 3:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._newton_meter = newton_meter
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                newton_meter = _np_.array(newton_meter, _np_.float32).flatten()
                if not newton_meter.size == 3:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'newton_meter: invalid array length: not {newton_meter.size} == 3')
                self._newton_meter = newton_meter
            assert isinstance(self._newton_meter, _np_.ndarray)
            assert self._newton_meter.dtype == _np_.float32
            assert self._newton_meter.ndim == 1
            assert len(self._newton_meter) == 3

    @property
    def newton_meter(self) -> _np_.ndarray:
        """
        saturated float32[3] newton_meter
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._newton_meter

    @newton_meter.setter
    def newton_meter(self, x: _ty_.Union[_np_.ndarray, _ty_.List[float]]) -> None:
        if isinstance(x, _np_.ndarray) and x.dtype == _np_.float32 and x.ndim == 1 and x.size == 3:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._newton_meter = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.float32).flatten()
            if not x.size == 3:  # Length cannot be checked before casting and flattening
                raise ValueError(f'newton_meter: invalid array length: not {x.size} == 3')
            self._newton_meter = x
        assert isinstance(self._newton_meter, _np_.ndarray)
        assert self._newton_meter.dtype == _np_.float32
        assert self._newton_meter.ndim == 1
        assert len(self._newton_meter) == 3

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Vector3_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        assert len(self.newton_meter) == 3, 'self.newton_meter: saturated float32[3]'
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.newton_meter)
        _ser_.pad_to_alignment(8)
        assert 96 <= (_ser_.current_bit_length - _base_offset_) <= 96, \
            'Bad serialization of uavcan.si.unit.torque.Vector3.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Vector3_1_0._DeserializerTypeVar_) -> Vector3_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "newton_meter"
        _f0_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.float32, 3)
        assert len(_f0_) == 3, 'saturated float32[3]'
        self = Vector3_1_0(
            newton_meter=_f0_)
        _des_.pad_to_alignment(8)
        assert 96 <= (_des_.consumed_bit_length - _base_offset_) <= 96, \
            'Bad deserialization of uavcan.si.unit.torque.Vector3.1.0'
        assert isinstance(self, Vector3_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'newton_meter=%s' % _np_.array2string(self.newton_meter, separator=',', edgeitems=10, threshold=1024, max_line_width=10240000),
        ])
        return f'uavcan.si.unit.torque.Vector3.1.0({_o_0_})'

    _EXTENT_BYTES_ = 12

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8CxcXB0{?YW-%r#)5I*D(5YQmT2aS;@#RuB^(Szcfnw%zulYrsPtlM_D-Oyj|Zcj==B8eJFHj#w&|8;sjJV0sEWZIee=9_P3'
        'zSe(#tJj8)ewr1b3?qw35S&K*i24y&BuL{dm0W?*3%g3>fyxDZC^9hT=EaFQHY<9HBs50<lbj9$npl!sdBT;YQt>$lYYzgn+D6Zi'
        '0SL*{#ITy4-W%EH#+&eJKg@~IbA&1-xSuPK=A*fZ(%&GXr@9=Xa7^V638|t)mHhPM8`6cKh0zbX{1C!TNcxJsDt}#VYJormF(hgP'
        'b_178@R%z;z=+vylu~sSWsdk<k!V=Nc+1Eypi+@I4Z*NS`r-CPdYNXuLEl#CLQQJl%?^?zQqd%&BD@Ur6LDhNM~(BaEW9shpioPR'
        '8h1xFV(8~>r_pj-ZD(z*?RHwO+u3lN&Gm-UblZ;Wbed}$t&Za~Oj#@U^(?Z>Xuwrryh&XreuRk6E*c*bKn>LOZ=>g5b5+T?i=QJ2'
        '^dw0$qnB?2kwxsM5f6-B+JZPmSxfToGY}M)W-R1w5-^UFW*vQh2QpCn|8cj-0di+AG45V3k0L6H>p_S$pivIyms#<a&!mr?*GbG1'
        '<9#X(dRQ9M<&g4-VuCkOM%K<G$_|GaO@@2h%l$HyP3idrzNj=IF(?oQA;J{<siC4&FI`$`;uqDW92>UD7A0;+2$_I@DhSP~zDxGY'
        'l_Xgz6yc%i=|v*bTm*oQ2uMb8_BymxoY@6E$kl48>FQCOIITe=va{SrC5eDO@<zz<Ey&dvR||w)U8pU&U0$eNU8p^}P^)P*tSSP>'
        'K^T=-Qj{lvJ3rt7m{YdJddy<Yp^(gB>y_-4-rF<`dD8!9DCl+Z__NAwyctxj>wRKx@qLFd-bhO84^U^9td9f$00'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

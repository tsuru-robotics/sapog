# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /home/silver/zubax/sapog/firmware/tools/testing_uavcan/public_regulated_data_types/uavcan/si/unit/volumetric_flow_rate/Scalar.1.0.uavcan
#
# Generated at:  2021-09-29 15:16:17.564498 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.si.unit.volumetric_flow_rate.Scalar
# Version:       1.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_


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
                 cubic_meter_per_second: _ty_.Optional[_ty_.Union[int, float, _np_.float32]] = None) -> None:
        """
        uavcan.si.unit.volumetric_flow_rate.Scalar.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param cubic_meter_per_second: saturated float32 cubic_meter_per_second
        """
        self._cubic_meter_per_second: float

        self.cubic_meter_per_second = cubic_meter_per_second if cubic_meter_per_second is not None else 0.0

    @property
    def cubic_meter_per_second(self) -> float:
        """
        saturated float32 cubic_meter_per_second
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._cubic_meter_per_second

    @cubic_meter_per_second.setter
    def cubic_meter_per_second(self, x: _ty_.Union[int, float, _np_.float32]) -> None:
        """Raises ValueError if the value is finite and outside of the permitted range, regardless of the cast mode."""
        x = float(x)
        in_range = -340282346638528859811704183484516925440.0 <= x <= 340282346638528859811704183484516925440.0
        if in_range or not _np_.isfinite(x):
            self._cubic_meter_per_second = x
        else:
            raise ValueError(f'cubic_meter_per_second: value {x} is not in [-340282346638528859811704183484516925440, 340282346638528859811704183484516925440]')

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Scalar_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        if _np_.isfinite(self.cubic_meter_per_second):
            if self.cubic_meter_per_second > 340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(340282346638528859811704183484516925440.0)
            elif self.cubic_meter_per_second < -340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(-340282346638528859811704183484516925440.0)
            else:
                _ser_.add_aligned_f32(self.cubic_meter_per_second)
        else:
            _ser_.add_aligned_f32(self.cubic_meter_per_second)
        _ser_.pad_to_alignment(8)
        assert 32 <= (_ser_.current_bit_length - _base_offset_) <= 32, \
            'Bad serialization of uavcan.si.unit.volumetric_flow_rate.Scalar.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Scalar_1_0._DeserializerTypeVar_) -> Scalar_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "cubic_meter_per_second"
        _f0_ = _des_.fetch_aligned_f32()
        self = Scalar_1_0(
            cubic_meter_per_second=_f0_)
        _des_.pad_to_alignment(8)
        assert 32 <= (_des_.consumed_bit_length - _base_offset_) <= 32, \
            'Bad deserialization of uavcan.si.unit.volumetric_flow_rate.Scalar.1.0'
        assert isinstance(self, Scalar_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'cubic_meter_per_second=%s' % self.cubic_meter_per_second,
        ])
        return f'uavcan.si.unit.volumetric_flow_rate.Scalar.1.0({_o_0_})'

    _EXTENT_BYTES_ = 4

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8L4#Cb0{?YW%TE+B7+)hR2tGm}T;(L-VP+q*I2^oa!es@C7;mQOwB4O1o#~{HWtW6R4jM?BXu{|J>o@G;BFZF_wE3RDN53xo'
        'YA!Uczwn}(aLZLhtT2))c}g=SBEoc0X)B$8@buUj&zv{n)1(q`1v}?(2HT-YN?Kt2m8T;{%gD;em(oQet$ZPzk&FzKJ|TuW5gjwC'
        'sDZFVM#5OBOUN5x@$>9_1^oy8#&<Y}utKQA+RQs);S1ci-=8E1&3!2ppYOFyICYe`dfEHRD<cc(<Onk!?<-B+-_TY_CLK|t9J(C('
        'o7j?3>qw!wfP6h{9Nm=HWzjo~9n>L&(f9@*A*>VYXvwMJw;NqxpMnmNBhTx>14EfZ_!eo|pPjKs*y<*&PTJ`vySv@A*GbdfUfOQI'
        'ZYAxso1{svy}Q@xB}ohFSw72~VT1V$=|<LtAr<~sFkNy83xsP1p@C^MtlgrPWRt0UXOM5@s}>=1Q5nHdEDo3985zj2;H1*V5y{~&'
        'tP-oeVFCk6kcuLpa1rOa5V4gCRgF(^$T+sN(!+QlO>shvh@IBT#yHW*a!96Di7THe+}DVqSM|WTVm6+oSQ*!DivQ=Pc<QF89krrq'
        'Iv}{5T3pMB($!**BolC%Z|6HmLZ*=8mp4|JOM;2+?j6FDx6-}8z8~XtW{U8T=nBH-eNF77$TWh&O%6n%(P*`tA5aYHw3%D$5n;JR'
        'yXI+lendG(R{lxK-_+4VuMp(qZWKF=sPY1Sz;=K0r_Jz9Rntb$U-B8kEo51{77uh>9~NupBGYyCG7;m7me<ej&}TODS@au<gmPvO'
        '1ONa'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

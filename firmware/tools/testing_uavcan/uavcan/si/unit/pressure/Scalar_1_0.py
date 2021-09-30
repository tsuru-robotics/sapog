# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/uavcan/si/unit/pressure/Scalar.1.0.uavcan
#
# Generated at:  2021-09-29 15:15:51.508058 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.si.unit.pressure.Scalar
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
                 pascal: _ty_.Optional[_ty_.Union[int, float, _np_.float32]] = None) -> None:
        """
        uavcan.si.unit.pressure.Scalar.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param pascal: saturated float32 pascal
        """
        self._pascal: float

        self.pascal = pascal if pascal is not None else 0.0

    @property
    def pascal(self) -> float:
        """
        saturated float32 pascal
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._pascal

    @pascal.setter
    def pascal(self, x: _ty_.Union[int, float, _np_.float32]) -> None:
        """Raises ValueError if the value is finite and outside of the permitted range, regardless of the cast mode."""
        x = float(x)
        in_range = -340282346638528859811704183484516925440.0 <= x <= 340282346638528859811704183484516925440.0
        if in_range or not _np_.isfinite(x):
            self._pascal = x
        else:
            raise ValueError(f'pascal: value {x} is not in [-340282346638528859811704183484516925440, 340282346638528859811704183484516925440]')

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Scalar_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        if _np_.isfinite(self.pascal):
            if self.pascal > 340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(340282346638528859811704183484516925440.0)
            elif self.pascal < -340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(-340282346638528859811704183484516925440.0)
            else:
                _ser_.add_aligned_f32(self.pascal)
        else:
            _ser_.add_aligned_f32(self.pascal)
        _ser_.pad_to_alignment(8)
        assert 32 <= (_ser_.current_bit_length - _base_offset_) <= 32, \
            'Bad serialization of uavcan.si.unit.pressure.Scalar.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Scalar_1_0._DeserializerTypeVar_) -> Scalar_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "pascal"
        _f0_ = _des_.fetch_aligned_f32()
        self = Scalar_1_0(
            pascal=_f0_)
        _des_.pad_to_alignment(8)
        assert 32 <= (_des_.consumed_bit_length - _base_offset_) <= 32, \
            'Bad deserialization of uavcan.si.unit.pressure.Scalar.1.0'
        assert isinstance(self, Scalar_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'pascal=%s' % self.pascal,
        ])
        return f'uavcan.si.unit.pressure.Scalar.1.0({_o_0_})'

    _EXTENT_BYTES_ = 4

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8CxcXB0{?YWOHUL*5MIMm@DU>MsGI~2%<N+phl3YQxU3)%<IQxsr<<LQJu{ttY*-Q!IcOy5L=(!t<nOYY1s5^Qsd}pF>-xU>'
        '`pfLE-!rYtFFe;{Zn;W`6-H7ePbgC&Aw^T^#!4q3JUn#97tR~;VXOsQz~&j8!bX@QHLWoJ%+pap>%_{$*U}~02y3xAIV`B62Erm4'
        '31ekbL)i)oAFtvI7~C7QzQGxUWkQ`Zl6faAe1f}X`db8HZdVG$r?V^(P8}sK4tQ6)HnNgVj<DkXu4<_Jm(DU_(h()<p(|mqhL8od'
        'j#Ld7P_Blj2iNVfEqQ~vy_iB8t*`JN!YZ+j)|?uC6X-kQRCI{Ccpfi4GPH0=-=ZwLS21FQ^<LKQ=G|Vlz1_?E-8}E_<ekpTcGk&z'
        'S)TPf+dJKUmbD??<ykow<~6k_Foapcn*u@$f79^fhLnVjCo4LIa=l!!NRbQNPC=dEa2_6!BY7-1(T#CLa@Y?m#5Ud(0uxFQO_4wl'
        'sjGB4rk}mrin4B<RCU%JwN<J;Q?ejN484kw(;e8Y3iS~tomeBaGL6<qudR_ztdVq*b}}geoV=tK?=+%zadRVC2ske{%1va*6bkm@'
        'daqM`vC!Q<LwN97y0@3-Lp)w>ILwenLs+{D#EvW0ARnA$PgD)MChq2)7KXaUOnov>ic+HY$~-(ipq$Hk_+L@^DrWb+LXzX#Swt97'
        '<punJjltSa%kY8d2@nhxJwv*ctfK`npvN&-h&Du#WA_pf$C}ocZ)o2$%REc|08vM&xX}Xu00'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

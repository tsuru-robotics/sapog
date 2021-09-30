# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /home/silver/zubax/sapog/firmware/tools/testing_uavcan/public_regulated_data_types/uavcan/node/IOStatistics.0.1.uavcan
#
# Generated at:  2021-09-29 15:16:17.836966 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.node.IOStatistics
# Version:       0.1
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class IOStatistics_0_1(_dsdl_.CompositeObject):
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
                 num_emitted:  _ty_.Optional[_ty_.Union[int, _np_.uint64]] = None,
                 num_received: _ty_.Optional[_ty_.Union[int, _np_.uint64]] = None,
                 num_errored:  _ty_.Optional[_ty_.Union[int, _np_.uint64]] = None) -> None:
        """
        uavcan.node.IOStatistics.0.1
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param num_emitted:  truncated uint40 num_emitted
        :param num_received: truncated uint40 num_received
        :param num_errored:  truncated uint40 num_errored
        """
        self._num_emitted:  int
        self._num_received: int
        self._num_errored:  int

        self.num_emitted = num_emitted if num_emitted is not None else 0

        self.num_received = num_received if num_received is not None else 0

        self.num_errored = num_errored if num_errored is not None else 0

    @property
    def num_emitted(self) -> int:
        """
        truncated uint40 num_emitted
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._num_emitted

    @num_emitted.setter
    def num_emitted(self, x: _ty_.Union[int, _np_.uint64]) -> None:
        """Raises ValueError if the value is outside of the permitted range, regardless of the cast mode."""
        x = int(x)
        if 0 <= x <= 1099511627775:
            self._num_emitted = x
        else:
            raise ValueError(f'num_emitted: value {x} is not in [0, 1099511627775]')

    @property
    def num_received(self) -> int:
        """
        truncated uint40 num_received
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._num_received

    @num_received.setter
    def num_received(self, x: _ty_.Union[int, _np_.uint64]) -> None:
        """Raises ValueError if the value is outside of the permitted range, regardless of the cast mode."""
        x = int(x)
        if 0 <= x <= 1099511627775:
            self._num_received = x
        else:
            raise ValueError(f'num_received: value {x} is not in [0, 1099511627775]')

    @property
    def num_errored(self) -> int:
        """
        truncated uint40 num_errored
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._num_errored

    @num_errored.setter
    def num_errored(self, x: _ty_.Union[int, _np_.uint64]) -> None:
        """Raises ValueError if the value is outside of the permitted range, regardless of the cast mode."""
        x = int(x)
        if 0 <= x <= 1099511627775:
            self._num_errored = x
        else:
            raise ValueError(f'num_errored: value {x} is not in [0, 1099511627775]')

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: IOStatistics_0_1._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        _ser_.add_aligned_unsigned(self.num_emitted, 40)
        _ser_.add_aligned_unsigned(self.num_received, 40)
        _ser_.add_aligned_unsigned(self.num_errored, 40)
        _ser_.pad_to_alignment(8)
        assert 120 <= (_ser_.current_bit_length - _base_offset_) <= 120, \
            'Bad serialization of uavcan.node.IOStatistics.0.1'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: IOStatistics_0_1._DeserializerTypeVar_) -> IOStatistics_0_1:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "num_emitted"
        _f0_ = _des_.fetch_aligned_unsigned(40)
        # Temporary _f1_ holds the value of "num_received"
        _f1_ = _des_.fetch_aligned_unsigned(40)
        # Temporary _f2_ holds the value of "num_errored"
        _f2_ = _des_.fetch_aligned_unsigned(40)
        self = IOStatistics_0_1(
            num_emitted=_f0_,
            num_received=_f1_,
            num_errored=_f2_)
        _des_.pad_to_alignment(8)
        assert 120 <= (_des_.consumed_bit_length - _base_offset_) <= 120, \
            'Bad deserialization of uavcan.node.IOStatistics.0.1'
        assert isinstance(self, IOStatistics_0_1)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'num_emitted=%s' % self.num_emitted,
            'num_received=%s' % self.num_received,
            'num_errored=%s' % self.num_errored,
        ])
        return f'uavcan.node.IOStatistics.0.1({_o_0_})'

    _EXTENT_BYTES_ = 15

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8L4#Cb0{@j&-D_M$6i={e>ZWSj)S^DvX$4IoxwoRe7Bwh_wP`R_e9>X<%-NlRduJ~5u^$1&J}3kR6gs~6*LvpO-DEY1;KH(V'
        '@A;kI`TEV-U#|UmXLGIl#QW`BI8hhWfmN(lC#<TWpxiXAamquAuN`|ExDOVd&s#_@)1w#Zr?e9{sAdh?-wJHPnJ%;uP#iov_RK5i'
        '6?ZA#pcAl88J*->-285Fewl`A!}Z_Nixjsg^WLf|cyQ?lB)uY?GgOKjUn;1@c^U&Mm}k`I+^%wOt!k846GUu(tDPEa5C_`B80<f5'
        '+M<>6v<5x)G7U31XU@|GOH1-@ymz!D%5KFz+MZ?;R<!<W`X<G@)On@_vtpI#G*ogUZt2iaKz9!!#cNa;p5pFv2?PxlSYk%R1<t{_'
        'QK;)VSzrlhk1@d&33+bynaXW>Z*h8ixFg?@@5=jqn439_1rC^{Nb*74`;QPy-2aTxmtw84eTculGE>qpjXCF+jz~5EVmJ>L5yc>9'
        '05irt5in93BN?4@dDy`p5^NcfNZ}>S39~@B2|Aaa&#Gx_XfQ#R-S#>L5W9n*YpjE~7PuNI&T>5qBQeNir^-RD2jcdM%xE?5g`4Xl'
        '^0xdyz9;wOqkzK~&|*he9?)rgosQHD1Z|D=REcyLZ&PQ2<$#77Xv=W4aZ*atK<QMCQZG+J#b%{rtr?diWt%A$P<mr(S7K<d^qBUy'
        'rEEi0D~^L2hdKv5SFtM>kbI%a)eBWTE<P-JBMO;H<}eA1oyl^aC=TgVKKOoTeQoVCveY4Q;B%|Tpz%s@qI4U4X@bX}4C<*_y=Xbk'
        '&P(Qdc-K-VO{fLY25GRwQEjHh;9x`;`S|f3ihSuvltXfEyHRCDA$U$2Ro6HMZnW4X2%h5e84u#g&mVn4=D@7$N%gt0laJfYq97Ai'
        '2k4!rmbD#-ctcLWnqtuDtAn`JbSpr8=kli#=hgA#mgYol&>DwP<a=1vxT)S>E{^kSi%s?aeopb`=gNQGJs;!aVsXS*sA*FqSCP1R'
        'QyCmLPVFf)2G>%S^0O9O?2SENKi4V8RPjnZiEkV+Auz=YAh|C;Jv%*#Z|)nN6{|0$jIZ{LD3ZKhS3JMCgl*WJ<l$9F%<2%=2D9@E'
        'ajw&@|LOO%Gu-*ZRk-@wz5rZ}p~5ydO6QG=2R6%x&Ae4n``LRyVb(I;{W~1uhWW8ige}>?RZ<L(B;a?12AM%T6JLCNx$g`?vsK?4'
        ';o@sog{t@)kEAp`9R~ma'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

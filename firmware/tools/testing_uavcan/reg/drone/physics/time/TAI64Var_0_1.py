# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/reg/drone/physics/time/TAI64Var.0.1.uavcan
#
# Generated at:  2021-09-29 15:15:52.530331 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     reg.drone.physics.time.TAI64Var
# Version:       0.1
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_
import reg.drone.physics.time


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class TAI64Var_0_1(_dsdl_.CompositeObject):
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
                 value:          _ty_.Optional[reg.drone.physics.time.TAI64_0_1] = None,
                 error_variance: _ty_.Optional[_ty_.Union[int, float, _np_.float32]] = None) -> None:
        """
        reg.drone.physics.time.TAI64Var.0.1
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param value:          reg.drone.physics.time.TAI64.0.1 value
        :param error_variance: saturated float32 error_variance
        """
        self._value:          reg.drone.physics.time.TAI64_0_1
        self._error_variance: float

        if value is None:
            self.value = reg.drone.physics.time.TAI64_0_1()
        elif isinstance(value, reg.drone.physics.time.TAI64_0_1):
            self.value = value
        else:
            raise ValueError(f'value: expected reg.drone.physics.time.TAI64_0_1 '
                             f'got {type(value).__name__}')

        self.error_variance = error_variance if error_variance is not None else 0.0

    @property
    def value(self) -> reg.drone.physics.time.TAI64_0_1:
        """
        reg.drone.physics.time.TAI64.0.1 value
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._value

    @value.setter
    def value(self, x: reg.drone.physics.time.TAI64_0_1) -> None:
        if isinstance(x, reg.drone.physics.time.TAI64_0_1):
            self._value = x
        else:
            raise ValueError(f'value: expected reg.drone.physics.time.TAI64_0_1 got {type(x).__name__}')

    @property
    def error_variance(self) -> float:
        """
        saturated float32 error_variance
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._error_variance

    @error_variance.setter
    def error_variance(self, x: _ty_.Union[int, float, _np_.float32]) -> None:
        """Raises ValueError if the value is finite and outside of the permitted range, regardless of the cast mode."""
        x = float(x)
        in_range = -340282346638528859811704183484516925440.0 <= x <= 340282346638528859811704183484516925440.0
        if in_range or not _np_.isfinite(x):
            self._error_variance = x
        else:
            raise ValueError(f'error_variance: value {x} is not in [-340282346638528859811704183484516925440, 340282346638528859811704183484516925440]')

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: TAI64Var_0_1._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        _ser_.pad_to_alignment(8)
        self.value._serialize_(_ser_)
        assert _ser_.current_bit_length % 8 == 0, 'Nested object alignment error'
        if _np_.isfinite(self.error_variance):
            if self.error_variance > 340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(340282346638528859811704183484516925440.0)
            elif self.error_variance < -340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(-340282346638528859811704183484516925440.0)
            else:
                _ser_.add_aligned_f32(self.error_variance)
        else:
            _ser_.add_aligned_f32(self.error_variance)
        _ser_.pad_to_alignment(8)
        assert 96 <= (_ser_.current_bit_length - _base_offset_) <= 96, \
            'Bad serialization of reg.drone.physics.time.TAI64Var.0.1'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: TAI64Var_0_1._DeserializerTypeVar_) -> TAI64Var_0_1:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "value"
        _des_.pad_to_alignment(8)
        _f0_ = reg.drone.physics.time.TAI64_0_1._deserialize_(_des_)
        assert _des_.consumed_bit_length % 8 == 0, 'Nested object alignment error'
        # Temporary _f1_ holds the value of "error_variance"
        _f1_ = _des_.fetch_aligned_f32()
        self = TAI64Var_0_1(
            value=_f0_,
            error_variance=_f1_)
        _des_.pad_to_alignment(8)
        assert 96 <= (_des_.consumed_bit_length - _base_offset_) <= 96, \
            'Bad deserialization of reg.drone.physics.time.TAI64Var.0.1'
        assert isinstance(self, TAI64Var_0_1)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'value=%s' % self.value,
            'error_variance=%s' % self.error_variance,
        ])
        return f'reg.drone.physics.time.TAI64Var.0.1({_o_0_})'

    _EXTENT_BYTES_ = 12

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8D1%gC0{^vEZEq7t5H^KCVkj-5?S~49Z9hPw#^;wfiIY+_DIzKu!b>7l6@_E(ZtPugw|ngFnHUMFd}syINkwAY-_)Pg*|i-9'
        '0+m{+mZO|^XJ(&$=9!uM<-{MfTJfLqVm?fCk_Mp$#c9f)(I|x=jAfQf%?;S{;~k@l*c1wOhdJ0ccHxD6Zs*IHP|ytbFDmE<iIM_>'
        'oDDUPbzpb~!S3eumG*tAY&jbaKxr<8WtH;O{qge~+pTnu{bpa-@^nazQ9LRPXuF58KY;4M%9b-*9MWWprWz*H(9k%D?4!{ln<+2+'
        '6FAFGvAGEdc4p7APsfhuKZGDxJmZEB5W%?}-WQNu7Y6#E-sa|X7;zJ(Ao_;c?gpZZsWxFI6GV5R{Nm0ejB^XF;@&N{<tX{p-m~Rr'
        'p*B<`R3(Q4y(}WU(n&-4N?X|SM3~6fmKzTQ6;eYiMY2b>51uuFl;#=|qPd8HG}l%ewMG-ayN$-W|NcynhrkvQEzciHK^P53xqWWg'
        'Jo{4PbrQ%G#MD4yUzKOW9^Z!~%%w6RPwaMiF4VG6G2liDVNMZj8P`pg*N60RVQP-b+OtfwTZ2Yg&x<JKafqoYQWtWXI$g_<3s803'
        'tNXOo$7!p(wAFpuf=18`3Oa}>l5jp`RO5*XgmJkV@EGhXw(!%R$19bcF^R<cZ4(!Rq%?w*%rj$hy<V@!Dj4R0k@b{E$ZXxS8!(fl'
        '3jw)XNCTv&WJU}FGP>k?wMtw>;&Y@)Pb#ttS+2>Zkr{td0CA#Ff*RC0O&7gyTquW;@WWd~0ZnTj)+FHp2EQ#}bbwDJ;hH4S<0v*l'
        'wGWmQ%10owN7kBat(B$b>S}}Js8xxGaMf8Un(&cXEb(xiV=ylIcz}`Kz$hxP$el$5<|%*}EkBinVK$UIlcX?!^dM$m$pRrES|nz?'
        '7K7$RMkwAs7*j)2Es4${<~<IYP~;E=<s20B0EvhpAX|k(cSRDe<3j84eY}^a2F1Y#+zcH7vM`z_;IO+y#4;Zr@5qsHks-H%OU&jd'
        '+2b_hE)|}0tkHu@HgGW^t%qpl;V5LqaY6|S$?zCusV3xm$Oy-`4Kl8FqDPLH4e90JJ~a>RP~IZwb0J)8*r%~chwjK0+G#Q=(FjmI'
        ';2o#dc%&;<7iw`Fn-Gr7xa&;sfK{Cq8k@-EHZ447y!0)R>R;f}XygM-aM2#B^uNIJQH~&6nj#CTu5(4Hw&kTskDc~7EMfERZ(E-E'
        'ft#ED_YVFXciHlID05qq4+YV~ERxt~ut(g2OkxLjLcfi&Mxm-{uRa;ZjN>R_>*XhRXyPj5h!OkV?QRz-3S;>0E=Cy8v;h0No$qeE'
        '))5Z8d=$ubXNw50n{naB06x%t_i)OM0#q4#cW0ej<+a8k0sFZtNF0vaMWiF&?q^1^*+N;tMm?QSI7a5SQc2BQlZSoPCG2Z<iCun)'
        '@iN*M+!Q!j$~i2+*b#ud&u)#M(XG6^)NZsot)=$L%2H>!)#)s+b(+o9M!VTrYIoYp&6Ty*a=YEIZZLU7XR%<U!aL(&#5#7+{(3MH'
        '&coJT^_trylifuW!$f!bNr8PjS)B9@-}gY{KWrvJ^}4`*<I5e}l$$lK*HLrS6y=FEBcvfiFoX^$PyKYRZsMY-`4<-_KF{3yqQP4b'
        'oqP-NSjeZs%|c+`I3n+|bL<h@DOl|l3$|Ik?EPQ!4BwFsk2KcA@x|`3CAQ*o%GTJG0~Kx_JY6}Y%+Ie%;jSp&EAet}q;TxI?&a#e'
        '(Y|9hy2miP-R=gviGR27+&d^jc5Q^=M<-H(+6L{69-+~rsnHE5^CQbnz`@@{r^`%i3IG5'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

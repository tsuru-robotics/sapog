# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /home/silver/zubax/sapog/firmware/tools/testing_uavcan/public_regulated_data_types/uavcan/si/sample/angular_acceleration/Vector3.1.0.uavcan
#
# Generated at:  2021-09-29 15:16:17.647958 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.si.sample.angular_acceleration.Vector3
# Version:       1.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_
import uavcan.time


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
                 timestamp:                    _ty_.Optional[uavcan.time.SynchronizedTimestamp_1_0] = None,
                 radian_per_second_per_second: _ty_.Optional[_ty_.Union[_np_.ndarray, _ty_.List[float]]] = None) -> None:
        """
        uavcan.si.sample.angular_acceleration.Vector3.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param timestamp:                    uavcan.time.SynchronizedTimestamp.1.0 timestamp
        :param radian_per_second_per_second: saturated float32[3] radian_per_second_per_second
        """
        self._timestamp:                    uavcan.time.SynchronizedTimestamp_1_0
        self._radian_per_second_per_second: _np_.ndarray

        if timestamp is None:
            self.timestamp = uavcan.time.SynchronizedTimestamp_1_0()
        elif isinstance(timestamp, uavcan.time.SynchronizedTimestamp_1_0):
            self.timestamp = timestamp
        else:
            raise ValueError(f'timestamp: expected uavcan.time.SynchronizedTimestamp_1_0 '
                             f'got {type(timestamp).__name__}')

        if radian_per_second_per_second is None:
            self.radian_per_second_per_second = _np_.zeros(3, _np_.float32)
        else:
            if isinstance(radian_per_second_per_second, _np_.ndarray) and radian_per_second_per_second.dtype == _np_.float32 and radian_per_second_per_second.ndim == 1 and radian_per_second_per_second.size == 3:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._radian_per_second_per_second = radian_per_second_per_second
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                radian_per_second_per_second = _np_.array(radian_per_second_per_second, _np_.float32).flatten()
                if not radian_per_second_per_second.size == 3:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'radian_per_second_per_second: invalid array length: not {radian_per_second_per_second.size} == 3')
                self._radian_per_second_per_second = radian_per_second_per_second
            assert isinstance(self._radian_per_second_per_second, _np_.ndarray)
            assert self._radian_per_second_per_second.dtype == _np_.float32
            assert self._radian_per_second_per_second.ndim == 1
            assert len(self._radian_per_second_per_second) == 3

    @property
    def timestamp(self) -> uavcan.time.SynchronizedTimestamp_1_0:
        """
        uavcan.time.SynchronizedTimestamp.1.0 timestamp
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, x: uavcan.time.SynchronizedTimestamp_1_0) -> None:
        if isinstance(x, uavcan.time.SynchronizedTimestamp_1_0):
            self._timestamp = x
        else:
            raise ValueError(f'timestamp: expected uavcan.time.SynchronizedTimestamp_1_0 got {type(x).__name__}')

    @property
    def radian_per_second_per_second(self) -> _np_.ndarray:
        """
        saturated float32[3] radian_per_second_per_second
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._radian_per_second_per_second

    @radian_per_second_per_second.setter
    def radian_per_second_per_second(self, x: _ty_.Union[_np_.ndarray, _ty_.List[float]]) -> None:
        if isinstance(x, _np_.ndarray) and x.dtype == _np_.float32 and x.ndim == 1 and x.size == 3:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._radian_per_second_per_second = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.float32).flatten()
            if not x.size == 3:  # Length cannot be checked before casting and flattening
                raise ValueError(f'radian_per_second_per_second: invalid array length: not {x.size} == 3')
            self._radian_per_second_per_second = x
        assert isinstance(self._radian_per_second_per_second, _np_.ndarray)
        assert self._radian_per_second_per_second.dtype == _np_.float32
        assert self._radian_per_second_per_second.ndim == 1
        assert len(self._radian_per_second_per_second) == 3

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Vector3_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        _ser_.pad_to_alignment(8)
        self.timestamp._serialize_(_ser_)
        assert _ser_.current_bit_length % 8 == 0, 'Nested object alignment error'
        assert len(self.radian_per_second_per_second) == 3, 'self.radian_per_second_per_second: saturated float32[3]'
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.radian_per_second_per_second)
        _ser_.pad_to_alignment(8)
        assert 152 <= (_ser_.current_bit_length - _base_offset_) <= 152, \
            'Bad serialization of uavcan.si.sample.angular_acceleration.Vector3.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Vector3_1_0._DeserializerTypeVar_) -> Vector3_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "timestamp"
        _des_.pad_to_alignment(8)
        _f0_ = uavcan.time.SynchronizedTimestamp_1_0._deserialize_(_des_)
        assert _des_.consumed_bit_length % 8 == 0, 'Nested object alignment error'
        # Temporary _f1_ holds the value of "radian_per_second_per_second"
        _f1_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.float32, 3)
        assert len(_f1_) == 3, 'saturated float32[3]'
        self = Vector3_1_0(
            timestamp=_f0_,
            radian_per_second_per_second=_f1_)
        _des_.pad_to_alignment(8)
        assert 152 <= (_des_.consumed_bit_length - _base_offset_) <= 152, \
            'Bad deserialization of uavcan.si.sample.angular_acceleration.Vector3.1.0'
        assert isinstance(self, Vector3_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'timestamp=%s' % self.timestamp,
            'radian_per_second_per_second=%s' % _np_.array2string(self.radian_per_second_per_second, separator=',', edgeitems=10, threshold=1024, max_line_width=10240000),
        ])
        return f'uavcan.si.sample.angular_acceleration.Vector3.1.0({_o_0_})'

    _EXTENT_BYTES_ = 19

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8L4#Cb0{^vFOK%*<5hf{7d`Z-Uk}ONI-Etg}OtiCnEwysuI0_xcMq8Aihb<&X#yvC5?S|%+?jDjWz({;ZAR+^J08aq@1pfpd'
        'gCqw7`2q1g7bCyG$5hSqESEBMi~#DZ>8`G-u4nHbkN@@E*^%mB{zlplbPzhO=1Q_qK4o6W9oJ8yG||%VGC%desLVH+;t%^NFTW@k'
        'KPx{i7xHm8W)bYSGPdKh*wNC_EK1=ti+fqfl*@ddhg>luli2x)`zBGVWj^WdaHV0X6eIb>N0$Dgq@#4?&*f)jKI1ZDl=L#gb@^M+'
        '^b#8fTxCAKDR~$i*f#A3%rMuW!D6gl6yy0dYpRhEcOLX(U#KLOPkHbV7PJBDOEDp)8cW1U&@Rr{<8v>wBULhzM(%(ebB|&zdod3_'
        'hz;*?b=YGwt|yHf^0;S2NxNXB&$Mx)BmgU~<`?fZg7BEL0eg3F3tjW4@_w10cfrOuU@90Ew4Zr!wV6ozD$(3e;-JiryFucYkN-P1'
        'GV)Mx5@(Ue6-l<q5SJ!KFhc~};Ur~R^MGg>`<&<`;)E$sp_uBE2tH#&WDNWjr*WoHs9gu4iIP3oUXTuVZd6?8VB#^&7m3s);M)>>'
        'LQ<|;EKNh{*C|0zjGrlmat23GQ>OVe1d4c^DE|8lVgtvwRT3RY*Msm?!bk*$adm@e&MPKA0l7Mbi^{kMt7=EW-6~ULrF|N10mkjH'
        'Fym;YNl46h&`t2)c9`te_6_zs>n(5z*_8p<$$bVkzCArnNQ<oeuCspFv%t>0Br{}XrQ0EW&Xm4Ec7^l>Zb6O2rtgs3WPPoYIdm56'
        '&LDRb*-f%A07amIkSvb5&$VVshW*+ENCYB{9#{)*gJWPVMx+B;jYu+$T$Os*4l)oy7-$2*d{2VEVgq?hd?mHiPJNk;5OP8Kt&Q7T'
        'WFbxr*?e!2KqkcCO9lFTrXVS@6#aFRczq~R)R?k<n6N6w5GZI2PG$JRCR8Ls^LxOo1q(xrFs55C<gJRmR<X?w92Id`sB_c|;s8l8'
        'Z!j&;2MTv%2n+!yYNv!kn9V0Qk{HXx4C+qIiPtT4jdsPG;w?IY^(5x&(wTU)MYryLyj6<D{Q9rCN?uf5<r~Bez40VYc4Mc^Pq>vq'
        'W&T>z6!=~W35U(>P)nG+U*#tY8+$}2pMop<xT;}))6%e?k1myHnf5Y|=W|1S(DnLtyTw~9h|6MCv@&QY0SBc}PCO|0^I3OW?(x9I'
        'K)Es~xAL>DPBP_l*a*3sGH4h1AKC&cx2<IenbUrnd2Fw(S(^0P+fqflO!2l!l2Ernt$_%+b<=F8nFp2YDvr$^6dtr#-L@>~sP>V4'
        ')me6yoSF-|q$`*PYq0KJTbboPc>iBpb)}<Zf|4;!pzsp~Z2-NC2@BQCpi<3lqMo#>QqV&ht6)_sAw`ThR9YY)3A4KRtJ*)%10O>6'
        '1QZvzGl`(H1y(U8s+WKyXiH7|t%`34coNmpDfi{J97=GQ3{SX&P1p+|z}K4uIq2DNY4hTDnV<ZHG#^&q5BMN^^J8w3mN|Ku5Z#Zw'
        '1mXf-y~Cr#cEh_Vj@?8Z%$^gjFQD#AaW6l8j|JEizsDpV;qF!z!tn0DxGOrJmkYF8Xb&cMT1zPDWahy=BN^j71A^@#F@ZA;vIK?F'
        'Q9L(N&@qe05XTC7+<uQEju!NUU7xV)lNP7!`ZVH+g3eg}lZcZAJ%xC@ptF|$G~!G_&)EI5h~ou4XXVTxo-62i#4`oGfH+&wi-;!+'
        '`U>K7K`+_!uUfsAt)44Z&Q+`LHN-0geI4;~LEk`pwV(v?QbDgFzEaRP5ib_>2Z$F6`WE8(g8mS3uAtYgUGs=%3%X$KTSPov&>vYl'
        'e~fslpf{|&Eqh<b+TBK+D(I56e;IM2peyzstJWWD_C8fyj}>&?-s`6IZ`a=MRvmZxw#A=V{HeuvEdI>myB2?L@qLSrEeeZ!7N1#s'
        'Zt+WtUs?Rx;x`t*wfJ3)cP2+Iaj78|8lu|}?>EHbh7b+0*AUMd;(0@S*$`hf#Mce+O+$R!5Z_rMgJ&I#0vI6J)9spv9UVr^lsR~4'
        'F6JXRu@0V>S6=eWRf_fD@wbV+z3vaUap~~e@{|itZG4c~NAJ~qY7+*sIm89?kHGv}5%bT$%82#gDU{*k^PPNtb!};-yRy2rzP{S+'
        'taQ7bTixa5n@elU-PN`3T4#Cv)=Fn>t)5R%^i%M5O_?uEzof^+2jauJN!%6phkD7m`#j}F9^H|~+$VVSk@(F}e<4NXsZZ!9g2A8n'
        'Y1#A-E&jGO@Z(j*0?A?*gt~QeA0olE;vX<T#cj0X@8YcZkN9UMHulAPTjH1bU;cmdPs?`w6R3UEPoTE_2{b$l#jp0!+M^x#@qik3'
        '>IHb<;KYxQ?DQBIZ1gZ&@wd~F(jEwxj#ggof|tAK<;uC@-(2JBb69<Tu<Bx$|K2i2!ucP=M|{9a4gdf'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)

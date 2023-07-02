# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

from cryptography import x509

#    CRLReason ::= ENUMERATED {
#        unspecified             (0),
#        keyCompromise           (1),
#        cACompromise            (2),
#        affiliationChanged      (3),
#        superseded              (4),
#        cessationOfOperation    (5),
#        certificateHold         (6),
#             -- value 7 is not used
#        removeFromCRL           (8),
#        privilegeWithdrawn      (9),
#        aACompromise           (10) }
_CRL_ENTRY_REASON_ENUM_TO_CODE = {
    x509.ReasonFlags.unspecified: 0,
    x509.ReasonFlags.key_compromise: 1,
    x509.ReasonFlags.ca_compromise: 2,
    x509.ReasonFlags.affiliation_changed: 3,
    x509.ReasonFlags.superseded: 4,
    x509.ReasonFlags.cessation_of_operation: 5,
    x509.ReasonFlags.certificate_hold: 6,
    x509.ReasonFlags.remove_from_crl: 8,
    x509.ReasonFlags.privilege_withdrawn: 9,
    x509.ReasonFlags.aa_compromise: 10,
}

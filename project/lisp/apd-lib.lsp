;;; apd-lib.lsp  Agentic PLC Design course helpers for AutoLISP.
;;; SAFE BY DEFAULT: nothing is changed unless *APD-APPLY* is T.
;;; Always run on a COPY of the drawing first. Plain AutoLISP only (no ActiveX).
;;; STATUS: written by an AI, UNTESTED in DraftSight until you run it (Module 4).

(setq *APD-APPLY* nil)

(defun apd-log (msg)
  (princ (strcat "\n[APD] " msg))
  (princ)
)

;; 0-based index of PAT in STR, or nil
(defun apd-search (pat str / i n m found)
  (setq i 1 n (strlen str) m (strlen pat) found nil)
  (if (> m 0)
    (while (and (not found) (<= (+ i m -1) n))
      (if (= (substr str i m) pat)
        (setq found (1- i))
        (setq i (1+ i))
      )
    )
  )
  found
)

(defun apd-str-replace (old new str / pos out)
  (setq out "")
  (while (setq pos (apd-search old str))
    (setq out (strcat out (substr str 1 pos) new)
          str (substr str (+ pos (strlen old) 1))
    )
  )
  (strcat out str)
)

;; Set attribute TAG on block reference INS to VAL
(defun apd-set-attrib (ins tag val / e ed done)
  (setq e (entnext ins) done nil)
  (while (and e (not done))
    (setq ed (entget e))
    (cond
      ((= (cdr (assoc 0 ed)) "SEQEND") (setq done T))
      ((and (= (cdr (assoc 0 ed)) "ATTRIB")
            (= (strcase (cdr (assoc 2 ed))) (strcase tag)))
       (apd-log (strcat tag ": '" (cdr (assoc 1 ed)) "' -> '" val "'"))
       (if *APD-APPLY* (entmod (subst (cons 1 val) (assoc 1 ed) ed)))
       (setq done T)
      )
    )
    (if (not done) (setq e (entnext e)))
  )
  (if *APD-APPLY* (entupdate ins))
  (princ)
)

;; Replace OLD with NEW in every single-chunk TEXT/MTEXT. Long MTEXT is stored in
;; several chunks and is NOT handled: check the count against what you expect.
(defun apd-replace-text (old new / ss i ed s s2 n)
  (setq n 0 ss (ssget "_X" '((0 . "TEXT,MTEXT"))))
  (if ss
    (progn
      (setq i 0)
      (while (< i (sslength ss))
        (setq ed (entget (ssname ss i))
              s  (cdr (assoc 1 ed))
              s2 (apd-str-replace old new s)
        )
        (if (/= s s2)
          (progn
            (apd-log (strcat "'" s "' -> '" s2 "'"))
            (setq n (1+ n))
            (if *APD-APPLY* (entmod (subst (cons 1 s2) (assoc 1 ed) ed)))
          )
        )
        (setq i (1+ i))
      )
    )
  )
  (apd-log (strcat (itoa n) " text object(s) " (if *APD-APPLY* "changed" "would change")))
  n
)

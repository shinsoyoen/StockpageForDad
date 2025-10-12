//------------/////// 이벤트 리스너 //////--------//
  document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ nav.js loaded and DOM ready!");

    // 테스트: 특정 버튼이나 요소가 실제로 존재하는지 확인
    console.log("🔍 checkAll:", document.getElementById("checkAll"));
    console.log("🔍 moveUp:", document.getElementById("moveUp"));
    console.log("🔍 deleteChois:", document.getElementById("deleteChois"));

    // ✅ DOM 요소 변수 선언
    const checkboxes = document.querySelectorAll('tbody input[type="checkbox"]');
    const checkAll = document.getElementById('checkAll');
    const moveUpTopButton = document.getElementById('moveUpTop');
    const moveUpButton = document.getElementById('moveUp');
    const moveDownButton = document.getElementById('moveDown');
    const moveDownBottomButton = document.getElementById('moveDownBottom');
    const tableBody = document.querySelector('tbody');
    const priceInput = document.getElementById("price");
    const quantityInput = document.getElementById("quantity");
    const deleteChois = document.getElementById("deleteChois");
    const categoryFilter = document.getElementById("categoryFilter");
    console.log("✅ nav.js loaded");
    const navLinks = document.querySelectorAll(".custom-tabs .nav-link");

    // ✅ 드롭다운 필터링
    if (categoryFilter) {
      categoryFilter.addEventListener("change", function () {
        const selected = this.value;
        const rows = document.querySelectorAll("tbody tr");

        rows.forEach(row => {
          const categoryCell = row.children[1]; // 두 번째 <td> (구분)
          if (!categoryCell) return;

          const cellText = categoryCell.textContent.trim();

          if (!selected || cellText === selected) {
            row.style.display = "";
          } else {
            row.style.display = "none";
          }
        });
      });
    }

    // ✅ 수정 버튼 활성화 
    document.querySelectorAll('.update-btn').forEach(button => {
      button.addEventListener('click', function () {

        // ✅ dataset에서 데이터 가져오기
        const tradeId = this.dataset.id;
        const category = this.dataset.category;
        const price = this.dataset.price;
        const quantity = this.dataset.quantity;
        const memo = this.dataset.memo;

        // ✅ 모달 내부 요소에 값 채워넣기
        const formMode = document.getElementById('form-mode');
        if (formMode) formMode.value = 'update';

        const tradeIdField = document.getElementById('form-trade-id');
        if (tradeIdField) tradeIdField.value = tradeId;

        const categoryField = document.querySelector('select[name="category"]');
        if (categoryField) categoryField.value = category;

        const priceField = document.querySelector('input[name="price"]');
        if (priceField) priceField.value = price;

        const quantityField = document.querySelector('input[name="quantity"]');
        if (quantityField) quantityField.value = quantity;

        const memoField = document.querySelector('input[name="memo"]');
        if (memoField) memoField.value = memo;

        const modalLabel = document.getElementById('tradeModalLabel');
        if (modalLabel) modalLabel.textContent = "✏️ 거래정보 수정";

        const modalElement = document.getElementById('tradeModal');
        if (modalElement) {
          const modal = new bootstrap.Modal(modalElement);
          modal.show();
        }
      });
    });

    // ✅ 개별 체크박스 변경 시 이벤트 등록
    checkboxes.forEach(cb => {
      cb.addEventListener('change', updateSelectedCount);
    });

    // ✅ 전체 선택 체크박스 클릭 시 동기화
    checkAll.addEventListener('change', () => {
      const isChecked = checkAll.checked;
      checkboxes.forEach(cb => cb.checked = isChecked);
      updateSelectedCount();
    });

    // ✅ 페이지 로드시 초기 선택 상태 반영
    updateSelectedCount();

    // ✅ 정렬 기준 로드 및 자동 정렬 실행
    const savedKey = localStorage.getItem("sortKey");
    const savedOrder = localStorage.getItem("sortOrder");

    if (savedKey && savedOrder) {
      document.getElementById("sortKey").value = savedKey;
      document.getElementById("sortOrder").value = savedOrder;
      document.getElementById("sortOrder").disabled = false;
      sortTable(); // 기본 sortKey, sortOrder가 적용됨
    }

    // ✅ 숫자만 입력 가능하도록 설정 및 콤마 포맷 적용
    const applyInitialFormat = (input) => {
      let value = input.value.replace(/[^0-9]/g, "");
      const formatted = value.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      input.value = formatted;
    };

    const formatWithComma = (input) => {
      input.addEventListener("keydown", function (e) {
        const allowedKeys = ["Backspace", "Delete", "ArrowLeft", "ArrowRight", "Tab"];
        if (!/[0-9]/.test(e.key) && !allowedKeys.includes(e.key)) {
          e.preventDefault();
        }
      });

      input.addEventListener("input", function (e) {
        let value = e.target.value.replace(/[^0-9]/g, "");
        const formatted = value.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        e.target.value = formatted;
        e.target.setSelectionRange(formatted.length, formatted.length);
      });
    };

    if (priceInput) {
      formatWithComma(priceInput);
      applyInitialFormat(priceInput);
    }
    if (quantityInput) {
      formatWithComma(quantityInput);
      applyInitialFormat(quantityInput);
    }

    // ✅ 부트스트랩 toast 알림 표시
    const toastElList = [].slice.call(document.querySelectorAll('.toast'));
    toastElList.forEach(function (toastEl) {
      const toast = new bootstrap.Toast(toastEl);
      toast.show();
    });

    // ✅ 정렬 기준 저장 후 자동 적용
    const tbody = document.querySelector("tbody");
    originalRows = Array.from(tbody.querySelectorAll("tr"));

    if (savedKey && savedOrder) {
      document.getElementById("sortKey").value = savedKey;
      document.getElementById("sortOrder").value = savedOrder;
      document.getElementById("sortOrder").disabled = false;
      sortTable(savedKey, savedOrder);
    }

    // ✅ 선택된 행들을 가져오는 함수
    function getCheckedRows() {
      return Array.from(tableBody.querySelectorAll('tr input[type="checkbox"]:checked'))
        .map(checkbox => checkbox.closest('tr'));
    }

    // ✅ 맨 위로 이동
    moveUpTopButton.addEventListener('click', () => {
      const checkedRows = getCheckedRows();
      checkedRows.forEach(row => {
        tableBody.prepend(row);
      });
    });

    // ✅ 위로 이동
    moveUpButton.addEventListener('click', () => {
      const checkedRows = getCheckedRows();
      checkedRows.forEach(row => {
        const previousSibling = row.previousElementSibling;
        if (previousSibling) {
          tableBody.insertBefore(row, previousSibling);
        }
      });
    });

    // ✅ 아래로 이동
    moveDownButton.addEventListener('click', () => {
      const checkedRows = getCheckedRows();
      for (let i = checkedRows.length - 1; i >= 0; i--) {
        const row = checkedRows[i];
        const nextSibling = row.nextElementSibling;
        if (nextSibling) {
          tableBody.insertBefore(nextSibling, row);
        }
      }
    });

    // ✅ 맨 아래로 이동
    moveDownBottomButton.addEventListener('click', () => {
      const checkedRows = getCheckedRows();
      // 뒤에서부터 순회하여 DOM 변경 시 인덱스 문제를 방지
      for (let i = checkedRows.length - 1; i >= 0; i--) {
        const row = checkedRows[i];
        tableBody.appendChild(row);
      }
    });

    // ✅ 삭제 버튼 누름 -> AJAX로 삭제
    document.querySelectorAll('.delete-btn').forEach(button => {
      button.addEventListener('click', function () {
        const tradeId = this.dataset.id;

        if (confirm("정말 이 거래를 삭제하시겠습니까?")) {
          fetch(`/delete/${tradeId}/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCSRFToken()
            },
          })
            .then(response => {
              if (response.ok) {
                this.closest('tr').remove();
                alert("✅ 성공적으로 삭제되었습니다!");
              } else {
                alert("❌ 삭제 실패");
              }
            })
            .catch(error => {
              console.error("🚨 삭제 중 오류:", error);
              alert("⚠️ 오류가 발생했습니다.");
            });
        }
      });

    });

    // ✅ row 선택-> 삭제 버튼 누르면 정보 삭제
    deleteChois.addEventListener('click', () => {
      const checkedRows = Array.from(document.querySelectorAll('tbody input[type="checkbox"]:checked'));

      if (checkedRows.length === 0) {
        alert("❗ 삭제할 항목을 선택해주세요.");
        return;
      }

      if (!confirm("선택한 거래를 모두 삭제하시겠습니까?")) return;

      checkedRows.forEach(cb => {
        const row = cb.closest('tr');
        const deleteBtn = row.querySelector('.delete-btn');
        const tradeId = deleteBtn.dataset.id;

        fetch(`/delete/${tradeId}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
          },
        })
          .then(response => {
            if (response.ok) {
              row.remove();
            } else {
              alert(`❌ 삭제 실패: 거래 ID ${tradeId}`);
            }
          })
          .catch(error => {
            console.error("🚨 삭제 중 오류:", error);
            alert("⚠️ 오류가 발생했습니다.");
          });
      });
      updateSelectedCount(); // 선택 개수 갱신
    });

    navLinks.forEach(link => {
        link.addEventListener("click", function () {
          navLinks.forEach(l => l.classList.remove("active"));
          this.classList.add("active");
        });
      });

    const currentPath = window.location.pathname;
      navLinks.forEach(link => {
        if (link.getAttribute("href") === currentPath) {
          link.classList.add("active");
        }
      });
      //
  });


  // ------ addEventListener 외부----------

  // ✅ 체크박스 갯수 count + 전체 선택 동기화 + 행 배경색 처리
  function updateSelectedCount() {
    const checkboxes = document.querySelectorAll('tbody input[type="checkbox"]');
    const count = [...checkboxes].filter(cb => cb.checked).length;
    document.getElementById('selected-count').innerText = `✔️ ${count}개 선택 중`;

    const checkAll = document.getElementById('checkAll');
    checkAll.checked = checkboxes.length > 0 && count === checkboxes.length;

    // ✅ 선택된 행에 배경색 클래스 토글
    checkboxes.forEach(cb => {
      const row = cb.closest('tr');
      if (cb.checked) {
        row.classList.add('highlight-row');
      } else {
        row.classList.remove('highlight-row');
      }
    });
  }

  // ✅ 거래 등록 폼 제출 시 유효성 검사 및 처리
  function submitTradeForm() {
    document.getElementById('tradeForm').submit();
    const form = document.getElementById("tradeForm");
    if (!form) {
      console.error("❌ tradeForm을 찾을 수 없습니다!");
      return;
    }

    const priceInput = document.getElementById("price");
    const quantityInput = document.getElementById("quantity");

    if (priceInput) priceInput.value = priceInput.value.replace(/,/g, "");
    if (quantityInput) quantityInput.value = quantityInput.value.replace(/,/g, "");

    const requiredFields = form.querySelectorAll("[required]");
    for (const field of requiredFields) {
      if (!field.value.trim()) {
        alert("⚠️ 모든 항목을 입력해주세요.");
        return;
      }
    }

    const confirmed = confirm("정말 거래를 등록하시겠습니까?");
    if (confirmed) {
      console.log("🟢 submit 시작");
      form.submit();
    }
  }

  // ✅ 정렬 드롭박스 (1번 선택 시 2번 활성화)
  function toggleSortOrder() {
    const sortKey = document.getElementById("sortKey").value;
    const sortOrder = document.getElementById("sortOrder");

    if (sortKey === "") {
      sortOrder.disabled = true;
      localStorage.removeItem("sortKey");
      localStorage.removeItem("sortOrder");
    } else {
      sortOrder.disabled = false;
      localStorage.setItem("sortKey", sortKey);
      sortTable(sortKey, document.getElementById("sortOrder").value);
    }
  }

  // ✅ 정렬 순서 변경 시 테이블 정렬
  function onSortOrderChange() {
    const sortKey = document.getElementById("sortKey").value;
    const sortOrder = document.getElementById("sortOrder").value;

    if (sortKey !== "") {
      localStorage.setItem("sortOrder", sortOrder);
      sortTable(sortKey, sortOrder);
    }
  }

  // ✅ 테이블 정렬 함수
  function sortTable(sortKey, sortOrder) {
    const tbody = document.querySelector("tbody");
    const rows = Array.from(tbody.querySelectorAll("tr"));

    const columnIndexMap = {
      "Date": 2,       // 날짜
      "price": 3,      // 매매가
      "quantity": 4,   // 수량
      "amount": 5      // 금액
    };
    
    const colIndex = columnIndexMap[sortKey];

    rows.sort((a, b) => {
      let aVal = a.children[colIndex].innerText.replace(/,/g, '');
      let bVal = b.children[colIndex].innerText.replace(/,/g, '');

      if (sortKey === "Date") {
        aVal = new Date(aVal);
        bVal = new Date(bVal);
      } else {
        aVal = parseFloat(aVal);
        bVal = parseFloat(bVal);
      }

      return sortOrder === 'asc' ? aVal - bVal : bVal - aVal;
    });

    rows.forEach(row => tbody.appendChild(row));
  }

  // ✅ 정렬 초기화 함수
  function resetSort() {
    localStorage.removeItem("sortKey");
    localStorage.removeItem("sortOrder");

    document.getElementById("sortKey").value = "";
    const orderSelect = document.getElementById("sortOrder");
    orderSelect.value = "asc";
    orderSelect.disabled = true;

    const tbody = document.querySelector("tbody");
    tbody.innerHTML = "";
    originalRows.forEach(row => tbody.appendChild(row));
  }

  // ✅ AJAX 삭제 토큰
  function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
  }
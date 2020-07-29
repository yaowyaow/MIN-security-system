<template>
    <div class="dialog">
        <el-dialog :title="dialog.title"
        :visible.sync="centerDialogVisible"
        :close-on-click-modal="false"
        :close-on-press-escape="false"
        :modal-append-to-body="false" 
        center>
        <span>dialog.full_log</span>
        <span slot="footer" class="dialog-footer">
        <el-button @click="centerDialogVisible = false">取 消</el-button>
        </span>
        </el-dialog>
    </div>
</template>
<script>
export default {
    name:'dialog',
    props: {
        dialog: Object, 
    },
    data(){
        return {
        centerDialogVisible: false
      };
    }
}
</script>

<style scoped>

</style>
